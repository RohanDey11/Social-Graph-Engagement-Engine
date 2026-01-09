<template>
    <Header />
        <h1>Welcome to Search Page</h1>
        <div class="add">
            <input type="text" v-model="search" placeholder="Enter name....." />
            <table>
                <tr v-for="item in filteredUsers" :key="item.id">
                    <td>{{ item.username }}</td>
                    <button v-if="this.followings.includes(item.id)" disabled>following</button>
                    <button v-else v-on:click="follow(item.id)">follow</button>

                </tr>
            </table>
        </div>
    </template>
    
    <script>
    import Header from './Header.vue'
    import axios from 'axios'
    export default {
        name:"Search",
        components:{
            Header
        },
        data()
        {
            return {
                users: [],
                search: "",
                currentid:"",
                followings:[],
                tokenr:''
            }
        },
        methods:{
            async follow(id)
            {
                let followid=id
                console.log("followid"+followid)
                try {
                    // Make a GET request to retrieve the user data
                    let response = await axios.get(`http://127.0.0.1:5000/user/${this.currentid}`,
                    {
                    headers:{
                        Authorization: `Bearer ${this.tokenr}`
                        }
                    });
                    // this.user=response.data
                    let data=response.data
                    let pretty=JSON.stringify(data)
                    console.log("pretty" + pretty)

                    this.name=JSON.parse(pretty).name;
                    this.username=JSON.parse(pretty).username
                    this.password=JSON.parse(pretty).password;
                    this.id=JSON.parse(pretty).id
                    this.following=JSON.parse(pretty).following
                    this.follower=JSON.parse(pretty).follower

                    // console.log(this.name)
                    // console.log(this.username)
                    // console.log(this.password) 
                    // console.log(this.id) 
                    // console.log(this.following)                


                    // Get the user's following array

                    // try 2 commenting below

                    let news=[]
                    if (this.following.trim() === '') {
                        news = []
                    } else if (this.following.indexOf(',') !== -1) {
                        news = this.following.split(',').map(Number)
                    } else {
                        news = [parseInt(this.following)]
                    }


                    this.followings = news
                    console.log(this.followings)
                    console.log("list")

                     // try 2

                    // Add the current user's ID to the followers array
                    this.followings.push(followid);
                    console.log(this.followings[0]+","+this.followings[1])

                    let nits=''

                    if (this.followings.length > 1) {
                        nits = this.followings.join(',')
                    } else if(this.followings.length==1) {
                        nits = this.followings[0].toString()
                    }
                    else{
                        nits=''
                    }
                    

                    const datas={
                        following: nits,
                        follower:this.follower
                    }
                    const formData=new FormData();
                    for (const key in datas){
                        formData.append(key,datas[key])
                    }
                    // Make a PUT request to update the user's followers array
                    const r1=await axios.put("http://127.0.0.1:5000/user/"+this.currentid,formData,
                    {
                    headers:{
                        Authorization: `Bearer ${this.tokenr}`
                        }
                    })
                    // if (r1.status==200)
                    // {
                    //     this.fetchUsers()
                    // }
                    // Log the followid to the console
                    console.log(`Followed user with ID: ${followid}`);
                // } catch (error) {
                //     console.error(error);
                //     }
                // // code for followers tab for followid user
                // try{
                    let responsef = await axios.get(`http://127.0.0.1:5000/user/${followid}`,
                    {
                    headers:{
                        Authorization: `Bearer ${this.tokenr}`
                        }
                    });
                    let dataf=responsef.data
                    let prettyf=JSON.stringify(dataf)
                    console.log("pretty" + prettyf)

                    this.name=JSON.parse(prettyf).name;
                    this.username=JSON.parse(prettyf).username
                    this.password=JSON.parse(prettyf).password;
                    this.id=JSON.parse(prettyf).id
                    this.following=JSON.parse(prettyf).following
                    this.follower=JSON.parse(prettyf).follower

                    console.log(this.name)
                    console.log(this.username)
                    console.log(this.password) 
                    console.log(this.id) 
                    console.log(this.following)
                    console.log(this.follower)
                    

                    // Get the user's follower array
                    let newes=[]
                    if (this.follower.trim() === '') {
                        newes = []
                    } else if (this.follower.indexOf(',') !== -1) {
                        newes = this.follower.split(',').map(Number)
                    } else {
                        newes = [parseInt(this.follower)]
                    }
                    let followers = newes
                    console.log(followers)
                    console.log("list")

                    // Add the current user's ID to the followers array
                    followers.push(this.currentid);
                    console.log("followers "+followers)

                    let nitss=''

                    if (followers.length > 1) {
                        nitss = followers.join(',')
                    } else if(followers.length==1) {
                        nitss = followers[0].toString()
                    }
                    else{
                        nitss=''
                    }

                    const datass={
                        following: this.following,
                        follower:nitss
                    }
                    const formDataa=new FormData();
                    for (const key in datass){
                        formDataa.append(key,datass[key])
                    }

                  // Make a PUT request to update the user's followers array
                    const r2=await axios.put("http://127.0.0.1:5000/user/"+followid,formDataa,
                    {
                    headers:{
                        Authorization: `Bearer ${this.tokenr}`
                        }
                    })

                    // try 3
                    // if (r2.status==200){
                    //     this.fetchUsers()
                    //     }

                    // try3

                    // Log the followid to the console
                    console.log(` user with ID: ${this.currentid} followed you`);
                    
                } catch (error){
                    console.error(error)
                }
            },
            async fetchUsers() {
                let user=localStorage.getItem('user-info');
                if(!user)
                {
                    this.$router.push({name:'SignUp'})
                }
                this.tokenr=JSON.parse(user).token
                this.currentid=JSON.parse(user).id;
                console.log(this.currentid)
                // try


                // try
                // this.following=JSON.parse(user).following
                // console.log(this.following)

                // if(!user){
                //     this.$router.push({name:'SignUp'})
                //     }

                try {
                    const response = await axios.get('http://127.0.0.1:5000/search',
                    {
                    headers:{
                        Authorization: `Bearer ${this.tokenr}`
                        }
                    });
                    this.users = response.data;
                    
                    // const responsef = await axios.get(`http://localhost:3000/users?id=${this.currentid}`)

                } catch (error) {
                    console.log(error);
                }
                const fdata=await axios.get(`http://127.0.0.1:5000/user/${this.currentid}`,
                {
                    headers:{
                        Authorization: `Bearer ${this.tokenr}`
                        }
                    })
                let t=fdata.data
                let a=t.following
                let b=[]
                    if (a.trim() === '') {
                        b = []
                    } else if (a.indexOf(',') !== -1) {
                        b = a.split(',').map(Number)
                    } else {
                        b = [parseInt(a)]
                    }
                this.followings=b
            }
        },
        computed: {
        filteredUsers() {
        return this.users.filter(user => user.username.toLowerCase().includes(this.search.toLowerCase()) && user.id !== this.currentid);
            }
        },
        async mounted() {
            this.fetchUsers();
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