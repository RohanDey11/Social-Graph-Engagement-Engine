<template>
<Header />
    <h1>Update your post</h1>
    <form class="add">
        <input type="text" name="title" placeholder="Enter title" v-model="post.title"/>
        <input type="text" name="caption" placeholder="Enter caption" v-model="post.caption"/>
        <!-- <input type="date" name="date" v-model="post.date" /> -->
        <button type="button" v-on:click="updatepost">Update</button>
    </form>

</template>

<script>
import Header from './Header.vue'
import axios from 'axios'
export default {
    name:"Update",
    components:{
        Header
    },
    data()
    {
        return {
            post :{
                title:'',
                image:'',
                caption:'',
                date:'',
                userid:''
            },
            tokenr:'',

        }
    },
    methods:{
        async updatepost()
        {
            console.warn(this.post)
            const datas={
                    title: this.post.title,
                    caption: this.post.caption,
                }
            const formData=new FormData();
            for (const key in datas){
                formData.append(key,datas[key])
            }
            const result=await axios.put("http://127.0.0.1:5000/post/u/"+this.$route.params.id,formData,
            {
            headers:{
                Authorization: `Bearer ${this.tokenr}`
                }
            })
            if (result.status==200)
            {
                this.$router.push({name:'Home'})
            }
        }
    },
    async mounted()
    {
        let user=localStorage.getItem('user-info');
        if(!user)
        {
            this.$router.push({name:'SignUp'})
        }
        this.userid=JSON.parse(user).id;
        this.tokenr=JSON.parse(user).token
        // if(!user)
        // {
        //     this.$router.push({name:'SignUp'})
        // }
        const result=await axios.get('http://127.0.0.1:5000/getPost/'+this.$route.params.id,
        {
        headers:{
            Authorization: `Bearer ${this.tokenr}`
            }
        })
        console.warn(result)
        this.post=result.data
    }
}
</script>