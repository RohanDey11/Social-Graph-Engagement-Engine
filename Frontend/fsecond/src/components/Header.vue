<template>
<div class="nav">
    <router-link to="/">Home</router-link >
    <router-link to="/add">Add Post</router-link >
    <router-link to="/search">Search</router-link>
    <router-link to="/profile">Profile</router-link>
    <router-link to="/following">Following</router-link>
    <router-link to="/follower">Follower</router-link>
    <a v-on:click="logout" href="#">Logout</a>
</div>
</template>

<script>
import axios from 'axios'
export default {
    name:'Header',
    methods:{
        async logout()
        
        {   
            let user=localStorage.getItem('user-info');
            let tokenr=JSON.parse(user).token
            console.log(tokenr)
            let b=JSON.parse(user).id
            let a=new Date().toLocaleString()
            console.log(a)
            console.log(b)
            const datas={
                    lasvi:a
                }
            const formData=new FormData();
            for (const key in datas){
                formData.append(key,datas[key])
            }
            const result=await axios.put("http://127.0.0.1:5000/user/"+b,formData,
            {
                headers:{
                    Authorization: `Bearer ${tokenr}`
                }
            })
            console.log(result)
            localStorage.clear();
            this.$router.push({name:'Login'})
        }
    }
}
</script>

<style>
.nav{
    background-color:#333;
    overflow:hidden;
}
.nav h2 {
    color:#ddd
}
.nav a {
    float: left;
    color: #f2f2f2f2;
    padding:14px 16px;
    text-align:center;
    font-size:17px;
    text-decoration:none;
    margin-right:5px;

}
.nav a:hover{
    background:#ddd;
    color:#333;
}
</style>