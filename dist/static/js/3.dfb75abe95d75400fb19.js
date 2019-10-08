webpackJsonp([3],{"6MCJ":function(e,t){},XfCb:function(e,t,a){"use strict";Object.defineProperty(t,"__esModule",{value:!0});var r={name:"sysRouterInfoManageList",data(){return{module_name:"sysRouterInfoManage",refresh_page_method:"refresh_"+this.module_name,project_type_code_list:null,project_env_code_list:null,project_state_code_list:null,project_team_code_list:null,searchFormData:{pageNum:1,pageSize:14,pageCount:1,order:"+router_path"},tableData:[]}},created(){this.$store.state.Apps.$on(this.refresh_page_method,()=>{this.search()})},async mounted(){this.search()},methods:{handleSizeChange(e){this.searchFormData.pageSize=e,this.search()},handleCurrentChange(e){this.searchFormData.pageNum=e,this.search()},onReset(){this.$refs.searchFormRef.resetFields(),this.search()},onSearch(){this.searchFormData.pageNum=1,this.search()},async search(){let e=await this.$search(this.searchFormData,"OAMP_search_sys_router_info_list");this.searchFormData.pageCount=e.pageCount,this.tableData=e.data},async onDelete(e,t){let a=t[e];this.$del(a,"OAMP_delete_sys_router_info")?(t.splice(e,1),this.$message.success("删除数据成功"),this.search()):this.$message.error("删除数据失败")}}},o={render:function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("div",{staticStyle:{"padding-top":"2px"}},[a("el-form",{ref:"searchFormRef",attrs:{inline:!0,model:e.searchFormData,size:"mini"}},[a("el-form-item",{attrs:{label:"路由显示名称",prop:"router_show_name"}},[a("el-input",{attrs:{placeholder:"请输入路由显示名称"},model:{value:e.searchFormData.router_show_name,callback:function(t){e.$set(e.searchFormData,"router_show_name",t)},expression:"searchFormData.router_show_name"}})],1),e._v(" "),a("el-form-item",{attrs:{label:"路由名称",prop:"router_name"}},[a("el-input",{attrs:{placeholder:"请输入路由名称"},model:{value:e.searchFormData.router_name,callback:function(t){e.$set(e.searchFormData,"router_name",t)},expression:"searchFormData.router_name"}})],1),e._v(" "),a("el-form-item",{attrs:{label:"创建时间",prop:"createTime"}},[a("el-date-picker",{attrs:{type:"daterange","range-separator":"至","start-placeholder":"开始日期","end-placeholder":"结束日期"},model:{value:e.searchFormData.createTime,callback:function(t){e.$set(e.searchFormData,"createTime",t)},expression:"searchFormData.createTime"}})],1),e._v(" "),a("div",{staticClass:"v-search-opt"},[a("div",{staticClass:"v-pagination"},[a("el-pagination",{attrs:{"current-page":e.searchFormData.pageNum,"page-size":e.searchFormData.pageSize,total:e.searchFormData.pageCount,"page-sizes":[14,20,50,100],layout:"total, sizes, prev, pager, next, jumper"},on:{"size-change":e.handleSizeChange,"current-change":e.handleCurrentChange}})],1),e._v(" "),a("div",{staticClass:"v-inline"},[a("el-button",{attrs:{size:"mini",type:"primary"},on:{click:e.onSearch}},[a("i",{staticClass:"iconfont icon-chaxun"}),e._v(" 查询")]),e._v(" "),a("el-button",{attrs:{size:"mini",type:"primary"},on:{click:e.onReset}},[a("i",{staticClass:"iconfont icon-chongzhi"}),e._v(" 重置")]),e._v(" "),a("el-button",{attrs:{size:"mini",type:"primary"},on:{click:function(t){return e.onAdd(e.module_name)}}},[a("i",{staticClass:"iconfont icon-xinzeng"}),e._v(" 新增")])],1)])],1),e._v(" "),a("hr"),e._v(" "),a("el-table",{attrs:{data:e.tableData,border:!0,stripe:!0,size:"mini",height:e.getTableHeight(130)}},[a("el-table-column",{attrs:{fixed:"",type:"index",index:e.onIndexMethod(e.searchFormData.pageNum,e.searchFormData.pageSize),label:"序号",width:"60"}}),e._v(" "),a("el-table-column",{attrs:{prop:"createTime",label:"创建时间",width:"156"}}),e._v(" "),a("el-table-column",{attrs:{"show-overflow-tooltip":!0,prop:"router_show_name",label:"显示名称",width:"110"}}),e._v(" "),a("el-table-column",{attrs:{"show-overflow-tooltip":!0,prop:"router_name",label:"路由名称",width:"110"}}),e._v(" "),a("el-table-column",{attrs:{prop:"router_has_icon",formatter:e.$format_bool,label:"附带图标",width:"80"}}),e._v(" "),a("el-table-column",{attrs:{label:"图标显示",width:"80"},scopedSlots:e._u([{key:"default",fn:function(e){return[a("i",{class:"iconfont "+e.row.router_icon_class})]}}])}),e._v(" "),a("el-table-column",{attrs:{"show-overflow-tooltip":!0,prop:"router_icon_class",label:"图标样式",width:"180"}}),e._v(" "),a("el-table-column",{attrs:{prop:"router_icon_size",width:"80",label:"图标尺寸"}}),e._v(" "),a("el-table-column",{attrs:{"show-overflow-tooltip":!0,prop:"router_path",label:"路由路径"}}),e._v(" "),a("el-table-column",{attrs:{fixed:"right",label:"操作",width:"160"},scopedSlots:e._u([{key:"default",fn:function(t){return[a("el-col",{attrs:{span:8}},[a("el-tooltip",{staticClass:"item",attrs:{effect:"dark",content:"查看",placement:"left"}},[a("el-button",{attrs:{type:"text",size:"small"},nativeOn:{click:function(a){return a.preventDefault(),e.onView(e.module_name,t.$index,e.tableData)}}},[a("i",{staticClass:"iconfont icon-chakan"})])],1)],1),e._v(" "),a("el-col",{attrs:{span:8}},[a("el-tooltip",{staticClass:"item",attrs:{effect:"dark",content:"修改",placement:"left"}},[a("el-button",{attrs:{type:"text",size:"small"},nativeOn:{click:function(a){return a.preventDefault(),e.onEdit(e.module_name,t.$index,e.tableData)}}},[a("i",{staticClass:"iconfont icon-xiugai"})])],1)],1),e._v(" "),a("el-col",{attrs:{span:8}},[a("el-tooltip",{staticClass:"item",attrs:{effect:"dark",content:"删除",placement:"left"}},[a("el-button",{attrs:{type:"text",size:"small"},nativeOn:{click:function(a){return a.preventDefault(),e.onDelete(t.$index,e.tableData)}}},[a("i",{staticClass:"iconfont icon-shanchu icon-red"})])],1)],1)]}}])})],1)],1)},staticRenderFns:[]};var s=a("VU/8")(r,o,!1,function(e){a("6MCJ")},"data-v-71dca0f2",null).exports,l={name:"sysRouterInfoManageInfo",data(){return{module_name:"sysRouterInfoManage",refresh_page_method:"refresh_"+this.module_name,mongodb_bool_type_code_list:null,pageData:{router_has_icon:"false"},pageDataRules:{router_show_name:[{required:!0,message:"请输入路由显示名称",trigger:"blur"}],router_name:[{required:!0,message:"请输入路由名称",trigger:"blur"}],router_path:[{required:!0,message:"请输入路由路径",trigger:"blur"}]}}},computed:{pageInfo(){return this.$setPageInfo(this.module_name)}},async mounted(){this.mongodb_bool_type_code_list=await this.$setCodeList(this.mongodb_bool_type_code_list,"mongodb_bool_type")},methods:{async onSubmit(){let e=this;this.$refs.pageDataRef.validate(async t=>{if(t){let t=this.pageData;null!=await e.$insert(t,"OAMP_insert_sys_router_info")?(e.$message.success("新增信息成功"),e.$onClose(e.module_name,"pageDataRef",e.refresh_page_method)):e.$message.error("新增信息失败")}})},async onUpdate(){let e=this;this.$refs.pageDataRef.validate(async t=>{if(t){let t=this.pageData;null!=await e.$update(t,"OAMP_update_sys_router_info")?(e.$message.success("修改信息成功"),e.$onClose(e.module_name,"pageDataRef",e.refresh_page_method)):e.$message.error("修改信息失败")}})}}},n={render:function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("el-dialog",{attrs:{title:"项目信息",visible:e.pageInfo.isShow,"modal-append-to-body":!1,"close-on-click-modal":!1,center:!0,"lock-scroll":!1},on:{close:function(t){return e.onClose(e.module_name,"pageDataRef")}}},[a("el-form",{ref:"pageDataRef",attrs:{model:e.pageData,rules:e.pageDataRules,inline:!0,"label-width":"160px",size:"small"}},[a("el-form-item",{attrs:{label:"路由显示名称",prop:"router_show_name"}},[a("el-input",{model:{value:e.pageData.router_show_name,callback:function(t){e.$set(e.pageData,"router_show_name",t)},expression:"pageData.router_show_name"}})],1),e._v(" "),a("el-form-item",{attrs:{label:" 路由名称",prop:"router_name"}},[a("el-input",{model:{value:e.pageData.router_name,callback:function(t){e.$set(e.pageData,"router_name",t)},expression:"pageData.router_name"}})],1),e._v(" "),a("el-form-item",{attrs:{label:"路由路径",prop:"router_path"}},[a("el-input",{staticStyle:{width:"696px"},model:{value:e.pageData.router_path,callback:function(t){e.$set(e.pageData,"router_path",t)},expression:"pageData.router_path"}})],1),e._v(" "),a("el-form-item",{attrs:{label:"是否有图标",prop:"router_has_icon"}},[a("el-select",{attrs:{placeholder:"请选择",clearable:""},model:{value:e.pageData.router_has_icon,callback:function(t){e.$set(e.pageData,"router_has_icon",t)},expression:"pageData.router_has_icon"}},e._l(e.mongodb_bool_type_code_list,function(e){return a("el-option",{key:e.codeId,attrs:{label:e.codeValue,value:e.codeId}})}),1)],1),e._v(" "),"true"===e.pageData.router_has_icon?a("el-form-item",{attrs:{label:"图标样式",prop:"router_icon_class"}},[a("el-input",{model:{value:e.pageData.router_icon_class,callback:function(t){e.$set(e.pageData,"router_icon_class",t)},expression:"pageData.router_icon_class"}})],1):e._e(),e._v(" "),a("el-form-item",{attrs:{label:"备注",prop:"remark"}},[a("el-input",{staticStyle:{width:"696px"},attrs:{type:"textarea"},model:{value:e.pageData.remark,callback:function(t){e.$set(e.pageData,"remark",t)},expression:"pageData.remark"}})],1)],1),e._v(" "),a("div",{staticClass:"dialog-footer",attrs:{slot:"footer"},slot:"footer"},[a("el-button",{on:{click:function(t){return e.onClose(e.module_name,"pageDataRef")}}},[e._v("关 闭")]),e._v(" "),"add"===e.pageInfo.pageModel?a("el-button",{attrs:{type:"primary"},on:{click:e.onSubmit}},[e._v("确 定")]):"edit"===e.pageInfo.pageModel?a("el-button",{attrs:{type:"primary"},on:{click:e.onUpdate}},[e._v("更 新")]):e._e()],1)],1)},staticRenderFns:[]};var i={name:"sysRouterInfoManage",components:{list:s,info:a("VU/8")(l,n,!1,function(e){a("rQZj")},"data-v-63ca71bd",null).exports}},c={render:function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("div",{staticClass:"v-container"},[a("el-breadcrumb",[a("el-breadcrumb-item",{attrs:{to:{name:"setting"}}},[e._v("设置")]),e._v(" "),a("el-breadcrumb-item",{attrs:{to:{name:"sysManage"}}},[e._v("系统管理")]),e._v(" "),a("el-breadcrumb-item",[e._v("系统路由信息管理")])],1),e._v(" "),a("hr"),e._v(" "),a("list"),e._v(" "),a("info")],1)},staticRenderFns:[]};var u=a("VU/8")(i,c,!1,function(e){a("ysG6")},"data-v-8e6b8bc0",null);t.default=u.exports},rQZj:function(e,t){},ysG6:function(e,t){}});
//# sourceMappingURL=3.dfb75abe95d75400fb19.js.map