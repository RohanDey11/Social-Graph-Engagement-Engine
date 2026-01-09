<template>
    <Header />
        <h1>People who you follow</h1>
        <div class="add">

            <table v-if="followingds.length">
                <tr>
                    <td>USERS</td>
                </tr>
                <tr v-for="item in followingds" :key="item.id">
                    <td><router-link :to="'/UserProfile/'+item.id">{{ item.username }}</router-link></td>
                    <button v-on:click="deletefollowing(item.id)">unfollow</button>
                </tr>

            </table>
            <h3 v-else>You don't follow anyone.Use the search tab to follow your friends and family.</h3>
        </div>
    </template>
    
    <script>
    import Header from './Header.vue'
    import axios from 'axios'
    export default {
        name:"Following",
        components:{
            Header
        },
        data()
        {
            return {
                followingds:[],
                tokenr:''
            }
        },
        methods:{
            async deletefollowing(d){
                console.log(this.userid)
                console.log(this.followingds)
                let i = this.followingds.map(item => item.id).indexOf(d) // find index of your object
                this.followingds.splice(i,1)
                console.log(this.followingds)

                // for loop to have a list of all ids inside followingds
                let ni=[]
                this.followingds.forEach(item => {
                    ni.push(item.id)
                })
                console.log(ni)

                let response = await axios.get(`http://127.0.0.1:5000/user/${this.userid}`,
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
                    this.follower=JSON.parse(pretty).follower

                    console.log(this.name)
                    console.log(this.username)
                    console.log(this.password) 
                    console.log(this.id) 
                    console.log(this.following)
                    console.log(this.follower)
                    
                    let nis=''
                    if (ni.length > 1) {
                        nis = ni.join(',')
                    } else if (ni.length==1){
                        nis = ni[0].toString()
                    }
                    else {
                        nis=''
                    }
                    console.log(nis)

                    const datas={
                        follower:this.follower,
                        following:nis
                    }
                    const formData=new FormData();
                    for (const key in datas){
                        formData.append(key,datas[key])
                    }

                    // Make a PUT request to update the user's followers array
                    const r1=await axios.put("http://127.0.0.1:5000/user/"+this.userid,formData,
                    {
                    headers:{
                        Authorization: `Bearer ${this.tokenr}`
                    }
                    })
                        // id: this.id,
                        // username: this.username,
                        // password: this.password,
                        // name:this.name,
                        // following:nis,
                        // follower:this.follower
                    // );



                    // unfollowed users follower list edit

                    let responsef = await axios.get(`http://127.0.0.1:5000/user/${d}`,
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

                    // let news = this.following.split(',').map(Number)
                    // console.log(news)
                    let news =[]
                    if (this.follower.indexOf(',') !== -1) {
                        news = this.follower.split(',').map(Number)
                    } else {
                        news = [parseInt(this.follower)]
                    }

                    console.log(news)

                    // Get the user's follower array

                    let it = news.map(item => item.id).indexOf(this.userid) // find index of your object
                    news.splice(it,1)
                    console.log(news)


                    let nits=''

                    if (news.length > 1) {
                        nits = news.join(',')
                    } else if(news.length==1) {
                        nits = news[0].toString()
                    }
                    else{
                        nits=''
                    }
                    console.log('below')
                    console.log(nits)

                    const datass={
                        following:this.following,
                        follower:nits
                    }
                    const formmData=new FormData();
                    for (const key in datass){
                        formmData.append(key,datass[key])
                    }
                    console.log(formmData)

                  // Make a PUT request to update the user's followers array
                    const r2=await axios.put("http://127.0.0.1:5000/user/"+d,formmData,
                    {
                    headers:{
                        Authorization: `Bearer ${this.tokenr}`
                        }
                    })
                        // id: this.id,
                        // username: this.username,
                        // password: this.password,
                        // name:this.name,
                        // following:this.following,
                    //     follower:nits
                    // );



            },
            async followingData(x){
                let response= await axios.get(`http://127.0.0.1:5000/user/${x}`,
                {
                headers:{
                    Authorization: `Bearer ${this.tokenr}`
                    }
                });
                let dataf=response.data
                // let pretty=JSON.stringyfy(data[0])
                // this.name=JSON.parse(pretty).name
                // console.log(this.name)
                console.log(dataf.name)
                let usernamef=dataf.username
                let followingd=[]
                followingd.push(dataf)
                console.log(followingd)
                this.followingds.push(dataf)
                console.log("result "+this.followingds)


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
            this.tokenr=JSON.parse(user).token
            // console.log(this.name)
            // console.log(this.userid)
            
            // if(!user)
            // {
            //     this.$router.push({name:'SignUp'})
            // }

            let response=await axios.get(`http://127.0.0.1:5000/user/${this.userid}`,
            {
                headers:{
                    Authorization: `Bearer ${this.tokenr}`
                    }
            });
            let data=response.data
            let pretty=JSON.stringify(data)
            console.log("pretty" + pretty)
            this.following=JSON.parse(pretty).following
            console.log(this.following)
            
            
            let a=this.following
            let b=[]
                if (a.trim() === '') {
                    b = []
                } else if (a.indexOf(',') !== -1) {
                    b = a.split(',').map(Number)
                } else {
                    b = [parseInt(a)]
                }
            console.log(b.length)

            if (b.length==0){
                this.followingds=[]
            }
            else{
                for (const i of b){
                    this.followingData(i)            
                }
            }
            

            


            // this.post=result.data;
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