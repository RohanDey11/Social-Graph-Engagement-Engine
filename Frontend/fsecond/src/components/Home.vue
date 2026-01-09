<template>
<Header />
    <h1>Home</h1>
    <main>
        <ul v-if="post.length">
        <li v-for="item in post" :key="item.id">
          <router-link :to="'/UserProfile/'+item.id"><h2 class="left-align">{{ item.namep }}</h2></router-link>
          <img :src="require(`../assets/${item.image}`)" alt="Item Image">
          <h2>{{item.title}}</h2>
          <p>{{item.caption}}</p>
          <p>{{item.date}}</p>
        </li>
        </ul>
        <h3 v-else>No Posts to Show .Follow other users and view their posts here.</h3>
    </main>
</template>

<script>
import Header from './Header.vue'
import axios from 'axios'
export default {
    name:"Home",
    data(){
        return {
            name:'',
            post:[],
            tokenr:''
        }
    },
    components:{
        Header
    },
    methods:{
        async postdata(x){
            let response= await axios.get(`http://127.0.0.1:5000/post/${x}`,
            {
                headers:{
                    Authorization: `Bearer ${this.tokenr}`
                }
            });
            var data1=response.data
            var data2=this.post
            var final=data2.concat(data1)
            this.post=final
        },
        async loadData()
        {
        let user=localStorage.getItem('user-info');
        if(!user)
        {
            this.$router.push({name:'SignUp'})
        }
        this.name=JSON.parse(user).name;
        let uid=JSON.parse(user).id
        this.tokenr=JSON.parse(user).token
        console.log(this.tokenr)
        console.log(this.name)
        
        const fdata=await axios.get(`http://127.0.0.1:5000/user/${uid}`,
          {
            headers:{
              Authorization: `Bearer ${this.tokenr}`
              }
          })
        let m=fdata.data
        this.following=m.following
        console.log(this.following)
        let n=this.following.split(',').map(Number)
            for (let i of n){
                this.postdata(i)            
            }





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
      /* .left-align {
        text-align: left;
        padding-left: 60px;
    } */

</style>