<template>
        <div>
  <v-container>
    <v-row>
      <v-col>
        <h1 class="text-center">{{status}}</h1>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" md="6" lg="4">
        <v-card>
          <v-card-title>登陆</v-card-title>
          <v-card-actions>
            <v-btn text color="primary" @click="$router.push('/login')">LOGIN</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
      <v-col cols="12" md="6" lg="4">
        <v-card>
          <v-card-title>文章管理</v-card-title>
          <v-card-actions>
            <v-btn text color="primary" @click="$router.push('/article')">GO</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
    <v-row v-if="access">
      <v-col>
        <h1 class="text-center">文章管理</h1>
      </v-col>
    </v-row>
    <v-row v-if="access">
      <v-col cols="12" md="6" lg="4" v-for="item in items" :key="item.id">
        <v-card>
          <v-card-title>{{item.title}}</v-card-title>
          <v-card-text>文章ID：{{item.id}}</v-card-text>
          <v-card-text v-if="item.decrypted">文章被加密</v-card-text>
          <v-card-actions>
            <v-btn text color="primary" @click="editArticle(item.id)">EDIT</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <h1 class="text-center">系统开发状态</h1>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" md="6" lg="4">
        <v-card>
          <v-card-title>博客管理</v-card-title>
          <v-card-text>
            管理Github博客<br>
            1. 文章查询-0%<br>
            2. 文章发布-0%<br>
            3. 文章列表<br>
            4. 文章删除<br>
            5. 文章导出-0%<br>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" md="6" lg="4">
        <v-card>
          <v-card-title>文章管理</v-card-title>
          <v-card-text>
            管理本地文章<br>
            1. 文章的增删改查<br>
            2. 文章加密<br>
            3. 文章导出<br>
            4. 文章发表形式渲染-0%<br>
          </v-card-text>
          
        </v-card>
      </v-col>
      <v-col cols="12" md="6" lg="4">
        <v-card>
          <v-card-title>文件管理和分享</v-card-title>
          <v-card-text>
            管理本地文件<br>
            1. 文件上传、下载<br>
            2. 文件共享<br>
            3. 文件打包迁移-50%未测试<br>
            4. 文件同步-0%<br>
            5. 文件加密-0%<br>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" md="6" lg="4">
        <v-card>
          <v-card-title>缓存配置管理</v-card-title>
          <v-card-text>对缓存的CURD</v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
  </div>

</template>

<script>
import http from '@/http'
export default {
  components:{},
  name: 'HomePage',
  data() {
    return {
      access: false,
      status: '尚未登陆',
      items: [],
  };
},
  methods:{
    fetchArticles(){
      http.get("/article/all").then(res => {
        if(res.status === 200){
          this.items = res.data
          this.access = true
          this.status = "您已登陆"
        }else{
          this.access = false
        }

      }).catch(err => {
        err;
        this.access = false;
      })
    },
    editArticle(id){
      this.$router.push("/new-article?id="+id);
    }
  },
  created(){
    this.fetchArticles()
  }
}
</script>

<style scoped>
/* 添加一些自定义样式 */
</style>
