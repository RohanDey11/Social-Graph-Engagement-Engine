<template>
    <Header />
        <h1>{{ username }}'s profile</h1>
        <h2>{{ name }}</h2>
        <main>
        <table>
            <tr>
                <td>Total Posts</td>
                <td>Followers</td>
                <td>Following</td>
            </tr>
            <tr>
                <td>{{ this.tpost }}</td>
                <td>{{this.tfollower}}</td>
                <td>{{this.tfollowing}}</td>

            </tr>
        </table>

        <ul>
        <li v-for="item in post" :key="item.id">
          <img :src="require(`../assets/${item.image}`)" alt="Item Image">
          <h2>{{item.title}}</h2>
          <p>{{item.caption}}</p>
          <p>{{item.date}}</p>
        </li>
        </ul>
    </main>
    </template>
    
    <script>
    import Header from './Header.vue'
    import axios from 'axios'
    export default {
        name:"UserProfile",
        data(){
            return {
                name:'',
                username:'',
                post:[],
                userid:'',
                tposts:'',
                tfollowing:'',
                tfollower:'',
                tpost:'',
                tokenr:''
            }
        },
        components:{
            Header
        },
        methods:{
            async loadData()
            {
            let userc=localStorage.getItem('user-info')
            if(!userc)
            {
                this.$router.push({name:'SignUp'})
            }
            this.tokenr=JSON.parse(userc).token

            let resultu=await axios.get('http://127.0.0.1:5000/user/'+this.$route.params.id,
            {
                headers:{
                    Authorization: `Bearer ${this.tokenr}`
                    }
                });
            console.warn(resultu)
            this.user=resultu.data;
            this.name=this.user.name
            this.username=this.user.username
            console.log(this.user.following)
            console.log(this.user.follower)

            let cfollowing=this.user.following
            let cfollower=this.user.follower
            if (cfollowing === '') {
                this.tfollowing=0;
            } else if (cfollowing.includes(',')) {
                this.tfollowing= cfollowing.split(',').length;
            } else {
                this.tfollowing= 1;
            }

            if (cfollower === '') {
                this.tfollower=0;
            } else if (cfollower.includes(',')) {
                this.tfollower= cfollower.split(',').length;
            } else {
                this.tfollower= 1;
            }
            let result=await axios.get('http://127.0.0.1:5000/post/'+this.$route.params.id,
            {
                headers:{
                    Authorization: `Bearer ${this.tokenr}`
                    }
                });
            console.warn(result)
            this.post=result.data;
            this.tpost=this.post.length
            }
        },
        async mounted()
        { 
            this.loadData()
        }
    }
    </script>
    
    <style>
    td{
        width:160px;
        height:40px;
    }
    </style>