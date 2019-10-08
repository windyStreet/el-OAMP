webpackJsonp([17],{"1LvK":function(e,t){},"9gNl":function(e,t){},Glp6:function(e,t){},IBwq:function(e,t,a){"use strict";Object.defineProperty(t,"__esModule",{value:!0});var n={name:"serverAgentManageList",data(){return{module_name:"serverAgentManage",refresh_page_method:"refresh_"+this.module_name,project_type_code_list:null,project_env_code_list:null,project_state_code_list:null,searchFormData:{pageNum:1,pageSize:14,pageCount:1,server_name:"",order:"+agent_name"},tableData:[]}},created(){this.$store.state.Apps.$on(this.refresh_page_method,()=>{this.search()})},async mounted(){this.search()},methods:{handleSizeChange(e){this.searchFormData.pageSize=e,this.search()},handleCurrentChange(e){this.searchFormData.pageNum=e,this.search()},onReset(){this.$refs.searchFormRef.resetFields(),this.search()},async r_search_list(e){let t=new this.$http,{data:a}=await t.post(e,"OAMP_search_agent_list");this.searchFormData.pageCount=a.pageCount,this.tableData=a.data},async r_delete_info(e){let t=new this.$http,{data:a}=await t.post(e,"OAMP_delete_agent_info");return null!=a&&"null"!==a},onSearch(){this.searchFormData.pageNum=1,this.search()},search(){let e=this.searchFormData;this.r_search_list(e)},on_agent_configure(e,t){this.$router.push({name:"agentConf",params:{serverId:t[e]._id}})}}},r={render:function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("div",[a("el-form",{ref:"searchFormRef",attrs:{inline:!0,model:e.searchFormData,size:"mini"}},[a("el-form-item",{attrs:{label:"代理服务器名称",prop:"project"}},[a("el-input",{attrs:{placeholder:"请输入代理服务器名称"},model:{value:e.searchFormData.server_name,callback:function(t){e.$set(e.searchFormData,"server_name",t)},expression:"searchFormData.server_name"}})],1),e._v(" "),a("div",{staticClass:"v-search-opt"},[a("div",{staticClass:"v-pagination"},[a("el-pagination",{attrs:{"current-page":e.searchFormData.pageNum,"page-size":e.searchFormData.pageSize,total:e.searchFormData.pageCount,"page-sizes":[14,20,50,100],layout:"total, sizes, prev, pager, next, jumper"},on:{"size-change":e.handleSizeChange,"current-change":e.handleCurrentChange}})],1),e._v(" "),a("div",{staticClass:"v-inline"},[a("el-button",{attrs:{size:"mini",type:"primary"},on:{click:e.onSearch}},[a("i",{staticClass:"iconfont icon-chaxun"}),e._v(" 查询")]),e._v(" "),a("el-button",{attrs:{size:"mini",type:"primary"},on:{click:e.onReset}},[a("i",{staticClass:"iconfont icon-chongzhi"}),e._v(" 重置")])],1)])],1),e._v(" "),a("hr"),e._v(" "),a("el-table",{attrs:{data:e.tableData,border:!0,stripe:!0,size:"mini",height:e.getTableHeight(130)}},[a("el-table-column",{attrs:{fixed:"",type:"index",index:e.onIndexMethod(e.searchFormData.pageNum,e.searchFormData.pageSize),label:"序号",width:"60"}}),e._v(" "),a("el-table-column",{attrs:{prop:"server_name",label:"代理服务器名称",width:"260"}}),e._v(" "),a("el-table-column",{attrs:{prop:"server_outer_ip",label:"代理外网ip",width:"180"}}),e._v(" "),a("el-table-column",{attrs:{prop:"server_inner_ip",label:"代理内网ip",width:"180"}}),e._v(" "),a("el-table-column",{attrs:{prop:"agent_network_area",label:"代理网段",width:"180"}}),e._v(" "),a("el-table-column",{attrs:{prop:"agent_location",label:"代理服务器位置",width:"280"}}),e._v(" "),a("el-table-column",{attrs:{prop:"agent_motor_room",label:"代理机房",width:"180"}}),e._v(" "),a("el-table-column",{attrs:{prop:"agent_safety_code",label:"代理安全码"}}),e._v(" "),a("el-table-column",{attrs:{fixed:"right",label:"操作",width:"60"},scopedSlots:e._u([{key:"default",fn:function(t){return[a("el-col",{attrs:{offset:"4",span:12}},[a("el-tooltip",{staticClass:"item",attrs:{effect:"dark",content:"代理配置",placement:"left"}},[a("el-button",{attrs:{type:"text",size:"small"},nativeOn:{click:function(a){return a.preventDefault(),e.on_agent_configure(t.$index,e.tableData)}}},[a("i",{staticClass:"iconfont icon-bushupeizhi"})])],1)],1)]}}])})],1)],1)},staticRenderFns:[]};var l=a("VU/8")(n,r,!1,function(e){a("Glp6")},"data-v-d7cd084c",null).exports,o={name:"serverAgentManageInfo",data(){return{module_name:"serverAgentManage",refresh_page_method:"refresh_"+this.module_name,project_type_code_list:null,project_env_code_list:null,project_state_code_list:null,pageData:{agent_server_id:"",agent_name:"",agent_outer_ip:"",agent_inner_ip:"",agent_location:"",agent_motor_room:"",agent_network_area:"",agent_safety_code:"",remark:""},pageDataRules:{agent_name:[{required:!0,message:"请输入代理名称",trigger:"blur"}]}}},computed:{pageInfo(){return this.$setPageInfo(this.module_name)}},methods:{async r_insert_info(e){let t=new this.$http,{data:a}=await t.post(e,"OAMP_insert_agent_info");if(null!=a&&"null"!==a)return a.data},async r_update_info(e){let t=new this.$http,{data:a}=await t.post(e,"OAMP_update_agent_info");if(null!=a&&"null"!==a)return a},onSubmit(){let e=this;this.$refs.pageDataRef.validate(async t=>{if(t){let t=this.pageData;null!=await e.r_insert_info(t)?(e.$message.success("新增代理信息成功"),e.$onClose(e.module_name,"pageDataRef",e.refresh_page_method)):e.$message.error("新增代理信息失败")}})},onUpdate(){let e=this;this.$refs.pageDataRef.validate(async t=>{if(t){let t=this.pageData;null!=await e.r_update_info(t)?(e.$message.success("修改代理信息成功"),e.$onClose(e.module_name,"pageDataRef",e.refresh_page_method)):e.$message.error("修改代理信息失败")}})}}},s={render:function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("el-dialog",{attrs:{title:"项目信息",visible:e.pageInfo.isShow,"modal-append-to-body":!1,"close-on-click-modal":!1,center:!0,"lock-scroll":!1},on:{close:function(t){return e.onClose(e.module_name,"pageDataRef")}}},[a("el-form",{ref:"pageDataRef",attrs:{model:e.pageData,rules:e.pageDataRules,inline:!0,"label-width":"160px",size:"small"}},[a("el-form-item",{attrs:{label:"代理服务器id",prop:"agent_server_id"}},[a("el-input",{staticStyle:{width:"260px"},model:{value:e.pageData.agent_server_id,callback:function(t){e.$set(e.pageData,"agent_server_id",t)},expression:"pageData.agent_server_id"}})],1),e._v(" "),a("el-form-item",{attrs:{label:"代理名称",prop:"agent_name"}},[a("el-input",{staticStyle:{width:"260px"},model:{value:e.pageData.agent_name,callback:function(t){e.$set(e.pageData,"agent_name",t)},expression:"pageData.agent_name"}})],1),e._v(" "),a("el-form-item",{attrs:{label:"代理网段",prop:"agent_network_area"}},[a("el-input",{staticStyle:{width:"260px"},model:{value:e.pageData.agent_network_area,callback:function(t){e.$set(e.pageData,"agent_network_area",t)},expression:"pageData.agent_network_area"}})],1),e._v(" "),a("el-form-item",{attrs:{label:"代理外网ip",prop:"agent_outer_ip"}},[a("el-input",{staticStyle:{width:"260px"},model:{value:e.pageData.agent_outer_ip,callback:function(t){e.$set(e.pageData,"agent_outer_ip",t)},expression:"pageData.agent_outer_ip"}})],1),e._v(" "),a("el-form-item",{attrs:{label:"代理内网ip",prop:"agent_inner_ip"}},[a("el-input",{staticStyle:{width:"260px"},model:{value:e.pageData.agent_inner_ip,callback:function(t){e.$set(e.pageData,"agent_inner_ip",t)},expression:"pageData.agent_inner_ip"}})],1),e._v(" "),a("el-form-item",{attrs:{label:"代理服务器位置",prop:"agent_location"}},[a("el-input",{staticStyle:{width:"260px"},model:{value:e.pageData.agent_location,callback:function(t){e.$set(e.pageData,"agent_location",t)},expression:"pageData.agent_location"}})],1),e._v(" "),a("el-form-item",{attrs:{label:"代理机房",prop:"agent_motor_room"}},[a("el-input",{staticStyle:{width:"260px"},model:{value:e.pageData.agent_motor_room,callback:function(t){e.$set(e.pageData,"agent_motor_room",t)},expression:"pageData.agent_motor_room"}})],1),e._v(" "),a("el-form-item",{attrs:{label:"代理安全码",prop:"agent_safety_code"}},[a("el-input",{staticStyle:{width:"260px"},model:{value:e.pageData.agent_safety_code,callback:function(t){e.$set(e.pageData,"agent_safety_code",t)},expression:"pageData.agent_safety_code"}})],1),e._v(" "),a("el-form-item",{attrs:{label:"备注",prop:"remark"}},[a("el-input",{staticStyle:{width:"660px"},attrs:{type:"textarea"},model:{value:e.pageData.remark,callback:function(t){e.$set(e.pageData,"remark",t)},expression:"pageData.remark"}})],1)],1),e._v(" "),a("div",{staticClass:"dialog-footer",attrs:{slot:"footer"},slot:"footer"},[a("el-button",{on:{click:function(t){return e.onClose(e.module_name,"pageDataRef")}}},[e._v("关 闭")]),e._v(" "),"add"===e.pageInfo.pageModel?a("el-button",{attrs:{type:"primary"},on:{click:e.onSubmit}},[e._v("确 定")]):"edit"===e.pageInfo.pageModel?a("el-button",{attrs:{type:"primary"},on:{click:e.onUpdate}},[e._v("更 新")]):e._e()],1)],1)},staticRenderFns:[]};var i={name:"serverAgentManage",components:{list:l,info:a("VU/8")(o,s,!1,function(e){a("9gNl")},"data-v-0828cdeb",null).exports}},p={render:function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("div",{staticClass:"v-container"},[a("el-breadcrumb",[a("el-breadcrumb-item",{attrs:{to:{name:"setting"}}},[e._v("设置")]),e._v(" "),a("el-breadcrumb-item",{attrs:{to:{name:"serverManage"}}},[e._v("服务器管理")]),e._v(" "),a("el-breadcrumb-item",[e._v("服务器代理管理")])],1),e._v(" "),a("hr"),e._v(" "),a("list"),e._v(" "),a("info")],1)},staticRenderFns:[]};var _=a("VU/8")(i,p,!1,function(e){a("1LvK")},"data-v-13eabe39",null);t.default=_.exports}});
//# sourceMappingURL=17.51793e01b6fb752b316a.js.map