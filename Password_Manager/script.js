// To show data in the table

const showPasswords = () =>{
    let tb =  document.querySelector('table')
    let data = localStorage.getItem("passwords")
    if (data==null){
        tb.innerHTML = "Nothing saved to show";
    }
    else{
        tb.innerHTML = `
        <tr>
        <th>Website</th>
        <th>Password</th>
        <th>Username</th>
        <th>Delete</th>
        </tr>
        `
        let arr =  JSON.parse(data);
        let str =  "";
        for(let i=0; i<arr.length;i++){
            const element =  arr[i];
        
            str += `<tr>
            <td>${element.website}</td>
            <td>${element.username}</td>
            <td>${element.password}</td>
            <td>${"delete"}</td>
            </tr>`
            
                   
        }
        tb.innerHTML = tb.innerHTML+str;

    }
}



showPasswords();
document.querySelector(".btn").addEventListener("click", (e)=>{
    e.preventDefault()
    console.log("clicked")
    let passwords = localStorage.getItem("passwords")
    console.log(passwords)
    if (passwords==null){
        let json = []
        json.push({username : Username.value, password : password.value})
        localStorage.setItem("passwords",JSON.stringify(json))
        alert("password stores in local");
    }
    else{
        let json = JSON.parse(localStorage.getItem("passwords"))
        json.push({website: Website.value,username : Username.value, password : password.value})
        localStorage.setItem("passwords",JSON.stringify(json))
        alert("password stores in local");
    }
    showPasswords();
})  