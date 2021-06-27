function register(phone, pass, pass2)
{
    if(pass != pass2)
    {
        alert("Passwords do not match");
    }
    else
    {
        alert(phone +"\n"+pass+"\n"+pass2);
    }
} 

