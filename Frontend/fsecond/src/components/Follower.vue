<template>
    <Header />
        <h1>People who follow you</h1>
        <div class="add">

            <table v-if="followerds.length">
                <tr>
                    <td>USERS</td>
                </tr>
                <tr v-for="item in followerds" :key="item.id">
                    <td>{{ item.username }}</td>
                    
                </tr>

            </table>
            <h3 v-else>You don't have any followers yet.</h3>

        </div>
    </template>
    
    <script>
    import Header from './Header.vue'
    import axios from 'axios'
    export default {
        name:"Follower",
        components:{
            Header
        },
        data()
        {
            return {
                followerds:[],
                currentid:[],
                tokenr:''
            }
        },
        methods:{
            async followb(y){
                console.log(y)
                
            },

            async followerData(x){
                let response= await axios.get(`http://127.0.0.1:5000/user/${x}`,
                {
                    headers:{
                        Authorization: `Bearer ${this.tokenr}`
                        }
                });
                let dataf=response.data

                console.log(dataf.name)
                let usernamef=dataf.username
                let followerd=[]
                followerd.push(dataf)
                console.log(followerd)
                this.followerds.push(dataf)
                console.log(this.followerds)


            },
            async loadData()
            {
            let user=localStorage.getItem('user-info');
            if(!user)
            {
                this.$router.push({name:'SignUp'})
            }
            this.name=JSON.parse(user).name;
            this.userid=JSON.parse(user).id
            this.currentid=this.userid
            this.tokenr=JSON.parse(user).token

            let response=await axios.get(`http://127.0.0.1:5000/user/${this.userid}`,
            {
                headers:{
                    Authorization: `Bearer ${this.tokenr}`
                    }
            });
            let data=response.data
            let pretty=JSON.stringify(data)
            console.log("pretty" + pretty)
            this.follower=JSON.parse(pretty).follower
            console.log(this.follower)
            
            let n =[]
            if (this.follower.indexOf(',') !== -1) {
                n = this.follower.split(',').map(Number)
            } else {
                n = [parseInt(this.follower)]
            }
            // let n=this.follower

            for (const i of n){
                this.followerData(i)            
            }
            
            console.log(this.followerds)


            }
        },
        async mounted()
        { 
            this.loadData()
        }
    }
    </script>

<style>
.user-list {
  list-style-type: none;
  padding: 0;
  margin: 0;
}

.user-list li {
  background-color: #f5f5f5;
  border-bottom: 1px solid #ddd;
  padding: 10px;
  font-size: 16px;
}

.user-list li:last-child {
  border-bottom: none;
}

.user-list li:hover {
  background-color: #e5e5e5;
  cursor: pointer;
}
</style>