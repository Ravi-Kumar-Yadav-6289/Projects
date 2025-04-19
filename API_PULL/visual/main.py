import requests, sqlite3
from type import TrialsResponse
from dataclasses import dataclass
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

query_condition = "SARS-CoV2"
query_other_term = ""
query_titles = ""
query_intervention = "Vaccination"

# TODO: max results = 1000, we need a loop if we need more, also the IP might be banned?
r = requests.get(
    f"https://clinicaltrials.gov/api/v2/studies?pageSize=1000&query.cond={query_condition}&query.term={query_other_term}&query.titles={query_titles}&query.intr={query_intervention}"
)
data: TrialsResponse = TrialsResponse.from_dict(r.json())
studies = data.studies

# print(data.studies[0].protocolSection.identificationModule.nctId.hasResults)


# print(r.json()["studies"][0]["hasResults"])


@dataclass
class Data:
    id: str
    research_title: str
    initiation_date: str
    status: str
    has_result: bool
    locations: tuple
    organization: str


extracted_data: list[Data] = []
country_count = {}

# TODO: locations also contain clinical trials locations (not just the research source)
for study in studies:
    countries = []
    if study.protocolSection.contactsLocationsModule is not None:
        countries = list(
            set(
                [
                    x.country
                    for x in study.protocolSection.contactsLocationsModule.locations
                    or []
                ]
            )
        )

    start_date = None
    if study.protocolSection.statusModule.startDateStruct is not None:
        start_date = study.protocolSection.statusModule.startDateStruct.date

    data = Data(
        id=study.protocolSection.identificationModule.nctId,
        research_title=study.protocolSection.identificationModule.officialTitle,
        initiation_date=start_date,
        status=study.protocolSection.statusModule.overallStatus.name,
        has_result=study.hasResults,
        locations=countries,
        organization=study.protocolSection.identificationModule.organization.fullName,
    )
    extracted_data.append(data)
    for c in countries:
        if c not in country_count:
            country_count[c] = 1
        else:
            country_count[c] += 1

# sort acc. to no. of researches
country_count_sorted = dict(
    sorted(country_count.items(), key=lambda item: item[1], reverse=True)
)

print(country_count_sorted)

# write to db
conn = sqlite3.connect("research.db")
df: pd.DataFrame = pd.DataFrame.from_records([x.__dict__ for x in extracted_data])
# convert locations array to a comma separated string
df["locations"] = df["locations"].apply(lambda x: ",".join(x))
df.to_sql("research", conn)


# visualization
# Set the aesthetic style of the plots
sns.set_style("whitegrid")
# Convert the country count dictionary to a DataFrame
country_df = pd.DataFrame(
    list(country_count_sorted.items()), columns=["Country", "Count"]
)

# Plot the top 10 countries with the most clinical trials
plt.figure(figsize=(14, 8))
sns.barplot(x="Count", y="Country", data=country_df.head(10), palette="viridis")
plt.title("Top 10 Countries by Number of Clinical Trials for SARS-CoV2 Vaccination")
plt.xlabel("Number of Clinical Trials")
plt.ylabel("Country")
plt.tight_layout()
plt.show()
