<template>
<Header />
    <h1>Create a new Post</h1>
    <div class="addPost">
        <input type="file" @change="onFileSelected">
        <br><br>
    <form class="add" >
        <input type="text" name="title" placeholder="Enter title" v-model="post.title"/>
        <input type="text" name="caption" placeholder="Enter caption" v-model="post.caption"/>
        <input type="date" name="date" v-model="post.date" />
        <!-- <input type="hidden" name="user_id" v-model="post.userid" />    -->
        <button type="button" v-on:click="addpost">Post</button>
    </form>
        <div v-if="error">
            <strong>{{ error }}</strong>
        </div>
    </div>
</template>

<script>
import Header from './Header.vue'
import axios from 'axios'
export default {
    name:"Add",
    components:{
        Header
    },
    data()
    {
        return {
            post :{
                title:'',
                caption:'',
                date:'',
                userid:'',
                namepo:'',
                
            },
            file:null,
            tokenr:'',
            error:null
        }
    },
    methods:{
        async addpost()
        {
            if (!this.post.title || !this.post.caption||!this.post.date||!this.file)
            {
                this.error="Add all fields to proceed"
            }
            else{
                console.warn(this.post)
                const data={
                    title: this.post.title,
                    caption: this.post.caption,
                    date: this.post.date,
                    userp_id:this.userid,
                    namep:this.post.namepo
                }
                const formData=new FormData();
                for (const key in data){
                    formData.append(key,data[key])
                }
                const result=await axios.post("http://127.0.0.1:5000/post", formData,
                {
                    headers:{
                        Authorization: `Bearer ${this.tokenr}`
                    }
                });
                if (result.status==200)
                {   
                    const resulto=await axios.get("http://127.0.0.1:5000/allPost",
                    {
                    headers:{
                        Authorization: `Bearer ${this.tokenr}`
                        }
                    })
                    console.log(resulto)
                    console.log(resulto.data.length)
                    let pid=resulto.data.length

                    const parts = this.file.name.split('.');
                    const extension = parts[1]

                    const formDataf = new FormData();
                    formDataf.append('file', this.file, `${pid}.${extension}`);
                    const response = await axios.post("http://127.0.0.1:5000/file-upload", formDataf,
                    {
                    headers:{
                        Authorization: `Bearer ${this.tokenr}`
                        }
                    });
                    console.log('Upload response:', response.data);

                    if (response.status==201)
                    {
                        const datai={
                            image:`${pid}.${extension}`
                        }
                        const formDatai=new FormData();
                        for (const key in datai){
                            formDatai.append(key,datai[key])
                        }
                        let resulti=await axios.put("http://127.0.0.1:5000/post/u/"+pid,formDatai,
                        {
                        headers:{
                            Authorization: `Bearer ${this.tokenr}`
                            }
                        })
                        if (resulti.status==200)
                        {
                            this.$router.push({name:'Home'})
                        }

                    }
                }
                console.warn("result",result)
            }
            


        },
        onFileSelected(event)
        {
            this.file = event.target.files[0];
            console.log(this.file.name)
            const parts = this.file.name.split('.');
            const extension = parts[1]
            console.log(extension)
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
        console.log(this.userid)
        this.tokenr=JSON.parse(user).token
        console.log(user)
        this.post.namepo=JSON.parse(user).username
    }
}
</script>