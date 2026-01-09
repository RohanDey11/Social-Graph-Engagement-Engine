<template>
    <Header />

        <h1>Hello {{name}}, Welcome to your profile</h1>
        <h2>{{ username }}</h2>
        <main>
        <table>
            <tr>
                <td>Total Posts</td>
                <td>Followers</td>
                <td>Following</td>
                <td><button v-on:click="csv_file()">CSV File</button></td>
            </tr>
            <tr>
                <td>{{ this.tpost }}</td>
                <td><router-link :to="'/follower'">{{this.tfollower}}</router-link></td>
                <td><router-link :to="'/following'">{{this.tfollowing}}</router-link></td>

            </tr>
        </table>
        <ul>
        <li v-for="item in post" :key="item.id">
          <img :src="require(`../assets/${item.image}`)" alt="Item Image">
          <h2>{{item.title}}</h2>
          <p>{{item.caption}}</p>
          <p>{{item.date}}</p>
          <router-link :to="'/update/'+item.id"><button>Update</button></router-link>
            <button v-on:click="deletepost(item.id)">Delete</button>
        </li>
        </ul>
        </main>
    </template>
    
    <script>
    import Header from './Header.vue'
    import axios from 'axios'

    export default {
        name:"Profile",
        data(){
            return {
                name:'',
                username:'',
                post:[],
                userid:'',
                tposts:'',
                tfollowing:'',
                tfollower:'',
                tpost:0,
                tokenr:''
            }
        },
        components:{
            Header
        },
        methods:{
            async csv_file(){
                let r=await axios.get(`http://127.0.0.1:5000/csv/${this.userid}`,
                {
                    headers:{
                        Authorization: `Bearer ${this.tokenr}`
                        }
                })
                console.warn(r)
            },
            async deletepost(id)
            {
                console.log(id)
                let result=await axios.delete(`http://127.0.0.1:5000/post/u/${id}`,
                {
                    headers:{
                        Authorization: `Bearer ${this.tokenr}`
                        }
                });
                console.warn(result)
                if(result.status==200)
                {
                    this.loadData()
                }
            },
            async loadData()
            {
            let user=localStorage.getItem('user-info');
            if(!user)
            {
                this.$router.push({name:'SignUp'})
            }
            let uid=JSON.parse(user).id
            this.name=JSON.parse(user).name;
            this.username=JSON.parse(user).username;
            this.userid=JSON.parse(user).id
            console.log(this.userid)
            this.tokenr=JSON.parse(user).token
            const fdata=await axios.get(`http://127.0.0.1:5000/user/${uid}`,
            {
                headers:{
                Authorization: `Bearer ${this.tokenr}`
                }
            })
            let m=fdata.data
            let cfollower=m.follower
            let cfollowing=m.following
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
            console.log(this.name)
            let result=await axios.get(`http://127.0.0.1:5000/post/${this.userid}`,
            {
                headers:{
                    Authorization: `Bearer ${this.tokenr}`
                    }
            });
            console.warn(result)
            this.post=result.data;
            console.log('l'+this.post.length)
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

    main {
        max-width: 800px;
        margin: 0 auto;
        padding: 20px;
      }
      
      ul {
        list-style: none;
        margin: 0;
        padding: 0;
      }
      
      li {
        border: 1px solid #dbdbdb;
        margin-bottom: 20px;
        padding: 10px;
      }
      
      img {
        display: block;
        margin: 0 auto;
        max-width: 100%;
      }
      
      h2, p {
        margin: 0;
        padding: 10px 0;
      }
      
      button {
        background-color: #0088cc;
        border: none;
        color: #fff;
        cursor: pointer;
        font-size: 14px;
        padding: 8px 16px;
        text-decoration: none;
      }
      
      button:hover {
        background-color: #006699;
      }
    
    </style>