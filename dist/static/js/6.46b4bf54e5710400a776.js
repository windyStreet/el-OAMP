webpackJsonp([6],{"+8pT":function(e,t){},C0IA:function(e,t){},"k/Y3":function(e,t,a){"use strict";Object.defineProperty(t,"__esModule",{value:!0});var r={name:"projectServiceContainerConfList",data(){return{module_name:"projectServiceContainerConf",refresh_page_method:"refresh_"+this.module_name,project_id:"",active:1,server_state_code_list:null,project_type_code_list:null,project_env_code_list:null,project_state_code_list:null,searchFormData:{pageNum:1,pageSize:13,pageCount:0},selected_server_table_data:[],selected_container_table_data:[],tableData:[],selected_server_id:"",project_info:{project:"",project_name:"",project_type_code_id:"",project_env_code_id:"",project_context:"",project_version:"",project_default_root_path:"",remark:""}}},async mounted(){this.project_id=this.$route.params.project_id,this.server_state_code_list=await this.$setCodeList(this.server_state_code_list,"server_state"),this.project_type_code_list=await this.$setCodeList(this.project_type_code_list,"project_type"),this.project_env_code_list=await this.$setCodeList(this.project_env_code_list,"project_env"),this.project_state_code_list=await this.$setCodeList(this.project_state_code_list,"project_state"),this.search_project_info(),this.search()},methods:{handleSizeChange(e){this.searchFormData.pageSize=e,this.search()},handleCurrentChange(e){this.searchFormData.pageNum=e,this.search()},onReset(){this.$refs.searchFormRef.resetFields(),this.search()},format_server_state_code_id(e,t,a){return this.$formatCodeValue(e,this.server_state_code_list,"server_state_code_id")},onSearch(){this.searchFormData.pageNum=1,this.search()},onNextStep(){this.active=2},async search(){this.search_project_server_list()},async search_project_info(){let e={project_id:this.project_id},t=await this.$search(e,"OAMP_search_project_info_by_id");this.project_info=t.data},async search_project_server_list(){let e=this.searchFormData;e.project_id=this.project_id;let t=await this.$search(e,"OAMP_search_project_server_list");this.searchFormData.pageCount=t.pageCount,this.tableData=t.data},async on_add_project_server_link(e,t){this.active=1;let a={link_id:this.project_id,linked_id:t[e]._id,link_type_code_id:"1"};null!==await this.$insert(a,"OAMP_insert_link_info")&&this.search()},async on_delete_project_server_link(e,t){this.active=1;let a={_id:t[e].link_info_id};!0===await this.$del(a,"OAMP_delete_link_info")?this.search():this.$message.error("删除关联服务器信息失败")},async search_selected_server_list(){let e={project_id:this.project_id},t=this.selected_server_table_data=await this.$search(e,"OAMP_search_server_list_by_project_id");this.selected_server_table_data=t.data,this.search()},async on_link_service_container(e,t){this.active=1,this.tableData=[],this.selected_server_id=t[e]._id;let a=this.searchFormData;a.belong_to_server_id=this.selected_server_id;let r=await this.$search(a,"OAMP_search_service_container_list");this.tableData=r.data},on_click_link_service_container(e,t){this.active=2},on_add_project_service_link(e,t){},on_delete_project_service_link(e,t){}}},i={render:function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("div",{staticStyle:{"padding-top":"2px"}},[a("el-row",{staticClass:"step"},[a("el-col",{attrs:{span:22}},[a("el-steps",{staticStyle:{height:"20px"},attrs:{active:e.active,simple:"","finish-status":"success"}},[a("el-step",{attrs:{title:"当前项目:"+e.project_info.project_name}}),e._v(" "),a("el-step",{attrs:{title:"选择服务器&服务容器"}}),e._v(" "),a("el-step",{attrs:{title:"完成"}})],1)],1)],1),e._v(" "),a("el-row",{attrs:{gutter:2}},[1===e.active?a("div",{staticStyle:{"padding-top":"2px"}},[a("el-form",{ref:"searchFormRef",attrs:{inline:!0,fit:!1,model:e.searchFormData,size:"mini"}},[a("el-form-item",{attrs:{label:"服务器名称",prop:"server_name"}},[a("el-input",{attrs:{placeholder:"请输入服务器名称"},model:{value:e.searchFormData.server_name,callback:function(t){e.$set(e.searchFormData,"server_name",t)},expression:"searchFormData.server_name"}})],1),e._v(" "),a("el-form-item",{attrs:{label:"服务器编号",prop:"server_no"}},[a("el-input",{attrs:{placeholder:"请输入服务器编号"},model:{value:e.searchFormData.server_no,callback:function(t){e.$set(e.searchFormData,"server_no",t)},expression:"searchFormData.server_no"}})],1),e._v(" "),a("div",{staticClass:"v-search-opt"},[a("div",{staticClass:"v-pagination"},[a("el-pagination",{attrs:{"current-page":e.searchFormData.pageNum,"page-size":e.searchFormData.pageSize,total:e.searchFormData.pageCount,"page-sizes":[13,20,50,100],layout:"total, sizes, prev, pager, next, jumper"},on:{"size-change":e.handleSizeChange,"current-change":e.handleCurrentChange}})],1),e._v(" "),a("div",{staticClass:"button-line"},[a("el-button",{attrs:{size:"mini",type:"primary"},on:{click:e.onSearch}},[a("i",{staticClass:"iconfont icon-chaxun"}),e._v(" 查询")]),e._v(" "),a("el-button",{attrs:{size:"mini",type:"primary"},on:{click:e.onReset}},[a("i",{staticClass:"iconfont icon-chongzhi"}),e._v(" 重置")]),e._v(" "),a("el-button",{attrs:{size:"mini",type:"primary"},on:{click:e.onNextStep}},[a("i",{staticClass:"iconfont icon-xiayibu"}),e._v(" 下一步")])],1)])],1),e._v(" "),a("hr"),e._v(" "),a("el-table",{attrs:{data:e.tableData,border:!0,stripe:!0,size:"mini",height:e.getTableHeight(130)}},[a("el-table-column",{attrs:{fixed:"",type:"index",index:e.onIndexMethod(e.searchFormData.pageNum,e.searchFormData.pageSize),label:"序号",width:"60"}}),e._v(" "),a("el-table-column",{attrs:{"show-overflow-tooltip":!0,prop:"server_name",label:"服务器名称",width:"160"}}),e._v(" "),a("el-table-column",{attrs:{prop:"server_no",label:"服务器编号",width:"160"}}),e._v(" "),a("el-table-column",{attrs:{formatter:e.format_server_state_code_id,prop:"server_state_code_id",label:"服务器状态",width:"90"}}),e._v(" "),a("el-table-column",{attrs:{prop:"server_shelf_time",label:"上架时间",width:"90"}}),e._v(" "),a("el-table-column",{attrs:{prop:"server_outer_ip",label:"外网ip",width:"140"}}),e._v(" "),a("el-table-column",{attrs:{prop:"server_inner_ip",label:"内网ip",width:"140"}}),e._v(" "),a("el-table-column",{attrs:{prop:"server_location",label:"服务器地址",width:"200","show-overflow-tooltip":!0}}),e._v(" "),a("el-table-column",{attrs:{prop:"remark",label:"备注"}}),e._v(" "),a("el-table-column",{attrs:{fixed:"right",label:"操作",width:"180"},scopedSlots:e._u([{key:"default",fn:function(t){return[a("el-col",{attrs:{span:11}},["0"===t.row.is_project_server_link?a("el-button",{attrs:{type:"primary",size:"mini"},nativeOn:{click:function(a){return a.preventDefault(),e.on_add_project_server_link(t.$index,e.tableData)}}},[e._v("添加关联")]):a("el-button",{attrs:{type:"info",size:"mini"},nativeOn:{click:function(a){return a.preventDefault(),e.on_delete_project_server_link(t.$index,e.tableData)}}},[e._v("移除关联")])],1),e._v(" "),a("el-col",{attrs:{offset:2,span:11}},["1"===t.row.is_project_server_link?a("el-button",{attrs:{type:"primary",size:"mini"},nativeOn:{click:function(a){return a.preventDefault(),e.onView(e.module_name,t.$index,e.tableData)}}},[e._v("关联服务")]):a("el-button",{attrs:{type:"warning",size:"mini"}},[e._v("关联服务")])],1)]}}],null,!1,2415699429)})],1)],1):e._e(),e._v(" "),2===e.active?a("div",{staticStyle:{"padding-top":"2px"}},[a("h1",[e._v("这里还能写点啥？？？？？？？？？")])]):e._e()])],1)},staticRenderFns:[]};var s=a("VU/8")(r,i,!1,function(e){a("C0IA")},"data-v-4b7e0196",null).exports,n={name:"selectServiceContainerList",data(){return{module_name:"projectServiceContainerConf",refresh_page_method:"refresh_"+this.module_name,service_container_type_code_list:null,service_container_state_code_list:null,project_id:"",pageData:{},searchFormData:{pageNum:1,pageSize:13,pageCount:0},tableData:[]}},watch:{pageData(){this.search()}},created(){this.$store.state.Apps.$on(this.refresh_page_method,()=>{this.search()})},computed:{pageInfo(){return this.project_id=this.$route.params.project_id,this.$setPageInfo(this.module_name)}},async mounted(){this.service_container_type_code_list=await this.$setCodeList(this.service_container_type_code_list,"service_container_type"),this.service_container_state_code_list=await this.$setCodeList(this.service_container_state_code_list,"service_container_state")},methods:{format_service_container_type(e,t,a){return this.$formatCodeValue(e,this.service_container_type_code_list,"service_container_type_code_id")},format_service_container_state(e,t,a){return this.$formatCodeValue(e,this.service_container_state_code_list,"service_container_state_code_id")},handleSizeChange(e){this.searchFormData.pageSize=e,this.search()},handleCurrentChange(e){this.searchFormData.pageNum=e,this.search()},onReset(){this.$refs.searchFormRef.resetFields(),this.search()},onSearch(){this.searchFormData.pageNum=1,this.search()},async search(){let e=this.searchFormData;e.project_id=this.project_id,e.belong_to_server_id=this.pageData._id;let t=await this.$search(e,"OAMP_search_project_server_container_list");this.searchFormData.pageCount=t.pageCount,this.tableData=t.data},async on_add_project_service_container_link(e,t){let a={link_id:this.project_id,linked_id:t[e]._id,link_type_code_id:"2"};null!==await this.$insert(a,"OAMP_insert_link_info")&&this.search()},async on_delete_project_service_container_link(e,t){let a={_id:t[e].link_info_id};!0===await this.$del(a,"OAMP_delete_link_info")?this.search():this.$message.error("删除关联服务器信息失败")}}},o={render:function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("el-dialog",{attrs:{title:"服务容器选择列表",width:"1250px",visible:e.pageInfo.isShow,"modal-append-to-body":!1,"close-on-click-modal":!1,center:!0,"lock-scroll":!1},on:{close:function(t){return e.onClose(e.module_name)}}},[a("el-form",{ref:"searchFormRef",attrs:{inline:!0,model:e.searchFormData,size:"mini"}},[a("el-form-item",{attrs:{label:"容器名称",prop:"service_container_name"}},[a("el-input",{attrs:{placeholder:"请输入容器名称"},model:{value:e.searchFormData.service_container_name,callback:function(t){e.$set(e.searchFormData,"service_container_name",t)},expression:"searchFormData.service_container_name"}})],1),e._v(" "),a("el-form-item",{attrs:{label:"创建时间",prop:"createTime"}},[a("el-date-picker",{attrs:{type:"daterange","range-separator":"至","start-placeholder":"开始日期","end-placeholder":"结束日期"},model:{value:e.searchFormData.createTime,callback:function(t){e.$set(e.searchFormData,"createTime",t)},expression:"searchFormData.createTime"}})],1),e._v(" "),a("div",{staticClass:"v-center"},[a("div",{staticClass:"v-inline"},[a("el-button",{attrs:{size:"mini",type:"primary"},on:{click:e.onSearch}},[a("i",{staticClass:"iconfont icon-chaxun"}),e._v(" 查询")]),e._v(" "),a("el-button",{attrs:{size:"mini",type:"primary"},on:{click:e.onReset}},[a("i",{staticClass:"iconfont icon-chongzhi"}),e._v(" 重置")]),e._v(" "),a("el-button",{attrs:{size:"mini",type:"primary"},on:{click:function(t){return e.onClose(e.module_name)}}},[a("i",{staticClass:"iconfont icon-guanbi"}),e._v(" 关闭")])],1)])],1),e._v(" "),a("hr"),e._v(" "),a("el-table",{attrs:{data:e.tableData,border:!0,stripe:!0,size:"mini",height:e.getTableHeight(360)}},[a("el-table-column",{attrs:{fixed:"",type:"index",index:e.onIndexMethod(e.searchFormData.pageNum,e.searchFormData.pageSize),label:"序号",width:"60"}}),e._v(" "),a("el-table-column",{attrs:{formatter:e.format_service_container_state,prop:"service_container_state_code_id",label:"运行状态",width:"100"}}),e._v(" "),a("el-table-column",{attrs:{"show-overflow-tooltip":!0,prop:"belong_to_server_id",label:"所属服务器id",width:"280"}}),e._v(" "),a("el-table-column",{attrs:{prop:"createTime",label:"创建时间",width:"160"}}),e._v(" "),a("el-table-column",{attrs:{"show-overflow-tooltip":!0,prop:"service_container_name",label:"容器名称",width:"160"}}),e._v(" "),a("el-table-column",{attrs:{prop:"service_container_port",label:"容器端口",width:"80"}}),e._v(" "),a("el-table-column",{attrs:{formatter:e.format_service_container_type,prop:"service_container_type_code_id",label:"容器类型"}}),e._v(" "),a("el-table-column",{attrs:{fixed:"right",label:"操作",width:"120"},scopedSlots:e._u([{key:"default",fn:function(t){return[a("el-col",{attrs:{span:24}},[a("el-col",{attrs:{span:11}},["0"===t.row.is_service_container_link?a("el-button",{attrs:{type:"primary",size:"mini"},nativeOn:{click:function(a){return a.preventDefault(),e.on_add_project_service_container_link(t.$index,e.tableData)}}},[e._v("添加容器关联")]):"1"===t.row.is_service_container_link?a("el-button",{attrs:{type:"info",size:"mini"},nativeOn:{click:function(a){return a.preventDefault(),e.on_delete_project_service_container_link(t.$index,e.tableData)}}},[e._v("移除容器关联")]):a("el-button",{attrs:{type:"danger",size:"mini"}},[e._v("容器已被关联")])],1)],1)]}}])})],1),e._v(" "),a("el-pagination",{attrs:{"current-page":e.searchFormData.pageNum,"page-size":e.searchFormData.pageSize,total:e.searchFormData.pageCount,"page-sizes":[13,20,50,100],layout:"total, sizes, prev, pager, next, jumper"},on:{"size-change":e.handleSizeChange,"current-change":e.handleCurrentChange}})],1)},staticRenderFns:[]};var c={name:"projectServiceContainerConf",components:{list:s,selectServiceContainerList:a("VU/8")(n,o,!1,function(e){a("yEIM")},"data-v-606cbf84",null).exports}},_={render:function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("div",{staticClass:"v-container"},[a("el-breadcrumb",[a("el-breadcrumb-item",{attrs:{to:{name:"setting"}}},[e._v("设置")]),e._v(" "),a("el-breadcrumb-item",{attrs:{to:{name:"projectManage"}}},[e._v("项目管理")]),e._v(" "),a("el-breadcrumb-item",{attrs:{to:{name:"projectClassManage"}}},[e._v("项目分类")]),e._v(" "),a("el-breadcrumb-item",[e._v("项目服务器容器配置")])],1),e._v(" "),a("hr"),e._v(" "),a("list"),e._v(" "),a("selectServiceContainerList")],1)},staticRenderFns:[]};var l=a("VU/8")(c,_,!1,function(e){a("+8pT")},"data-v-4958547a",null);t.default=l.exports},yEIM:function(e,t){}});
//# sourceMappingURL=6.46b4bf54e5710400a776.js.map