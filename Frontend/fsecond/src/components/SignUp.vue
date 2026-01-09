<template>
    <h1>Sign up</h1>
    <div class="register">
        <input type="text" v-model="username" placeholder="Enter Username" >
        <input type="text" v-model="password" placeholder="Enter password"  >
        <input type="text" v-model="name" placeholder="Enter name" >
        <input type="text" v-model="email" placeholder="Enter email"> 
        <button v-on:click="signUp">Sign Up</button>
        <p>
            <router-link to="/Login" >Login</router-link>
        </p>
        <div v-if="error">
            <strong>{{ error }}</strong>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
export default {
    name:'SignUp',
    data()
    {
        return{
            username:'',
            password:'',
            name:'',
            email:'',
            error:null
        }
    },
    methods:{
        async signUp()
        {
            if (!this.username || !this.password || !this.name|| !this.email)
            {
                this.error="Add all fields to proceed"
            }
            else{
                const data={
                name:this.name,
                username:this.username,
                password:this.password,
                email:this.email
                }
                const formData=new FormData();
                for (const key in data){
                    formData.append(key,data[key])
                }
                let result=await axios.post("http://127.0.0.1:5000/user",formData);

                console.warn(result)
                if(result.status==200)
                {
                    this.$router.push({name:'Login'})
                }
            }

        }
    },
    mounted()
    {
        let user=localStorage.getItem('user-info');
        if(user)
        {
            this.$router.push({name:'Home'})
        }
    }
}
</script>

<style>
.register input{
    width:300px;
    height:40px;
    padding-left: 20px;
    display:block;
    margin-bottom:30px;
    margin-right:auto;
    margin-left:auto;
    border:1px solid skyblue;
}
.register button {
    width:320px;
    height:40px;
    border:1px solid skyblue;
    background: skyblue;
    color: #fff;
    cursor:pointer;
}
</style>