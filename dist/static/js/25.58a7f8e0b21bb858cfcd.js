webpackJsonp([25],{"4n49":function(e,r,t){"use strict";Object.defineProperty(r,"__esModule",{value:!0});var n={name:"userLogin",data:()=>({LoginForm:{userName:"",password:""},logining:!1,rule:{userName:[{required:!0,max:14,min:2,message:"用户名是必须的，长度为2-14位",trigger:"blur"}],password:[{required:!0,message:"密码是必须的！",trigger:"blur"}]}}),methods:{async r_userLogin(e){let r=new this.$http,{data:t}=await r.post(e,"OAMP_userLogin");return null!=t&&"null"!==t?t:null},onLogin(){this.$refs.LoginForm.validate(async e=>{let r=this;if(e){r.logining=!0;let e={userName:this.LoginForm.userName,password:this.LoginForm.password},t=await r.r_userLogin(e);null==t?(r.$message.error("登录名或密码错误"),r.logining=!1):(r.$store.commit("setUserInfo",t),r.$store.commit("setIsLogin",!0),location.reload())}else this.$message.error("登录错误")})},reset(){this.$refs.LoginForm.resetFields()}}},o={render:function(){var e=this,r=e.$createElement,t=e._self._c||r;return t("el-form",{ref:"LoginForm",staticClass:"login-form",attrs:{model:e.LoginForm,rules:e.rule,"label-width":"0"},nativeOn:{keyup:function(r){return!r.type.indexOf("key")&&e._k(r.keyCode,"enter",13,r.key,"Enter")?null:e.onLogin(r)}}},[t("h3",[e._v("用户登录")]),e._v(" "),t("el-form-item",{attrs:{prop:"userName"}},[t("el-input",{attrs:{type:"text",placeholder:"填写自己的姓名，不支持昵称登录"},model:{value:e.LoginForm.userName,callback:function(r){e.$set(e.LoginForm,"userName",r)},expression:"LoginForm.userName"}})],1),e._v(" "),t("el-form-item",{attrs:{prop:"password"}},[t("el-input",{attrs:{type:"password",placeholder:"用户密码"},model:{value:e.LoginForm.password,callback:function(r){e.$set(e.LoginForm,"password",r)},expression:"LoginForm.password"}})],1),e._v(" "),t("el-form-item",[t("el-button",{staticClass:"submitBtn",attrs:{type:"danger",round:"",loading:e.logining},nativeOn:{click:function(r){return r.preventDefault(),e.onLogin(r)}}},[e._v("登录")]),e._v(" "),t("el-button",{staticClass:"resetBtn",attrs:{type:"primary",round:""},nativeOn:{click:function(r){return r.preventDefault(),e.reset(r)}}},[e._v("重置")]),e._v(" "),t("hr"),e._v(" "),t("p",[e._v("还没有账号，马上去联系管理员")])],1)],1)},staticRenderFns:[]};var s=t("VU/8")(n,o,!1,function(e){t("OTN+")},"data-v-7e4f614a",null);r.default=s.exports},"OTN+":function(e,r){}});
//# sourceMappingURL=25.58a7f8e0b21bb858cfcd.js.map