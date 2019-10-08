webpackJsonp([20],{"3kxu":function(e,t){},"4+jE":function(e,t,a){"use strict";Object.defineProperty(t,"__esModule",{value:!0});var o={name:"sysRouterInfoManageNodeInfo",data(){return{module_name:"sysRouterInfoManageNode",refresh_page_method:"refresh_"+this.module_name,mongodb_bool_type_code_list:null,pageData:{},pageDataRules:{router_show_name:[{required:!0,message:"请输入路由显示名称",trigger:"blur"}],router_name:[{required:!0,message:"请输入路由名称",trigger:"blur"}],router_path:[{required:!0,message:"请输入路由路径",trigger:"blur"}]}}},watch:{"pageData.router_show_name":{handler(e,t){this.pageData.label=e},deep:!0,immediate:!0}},computed:{pageInfo(){let e=this.$setPageInfo(this.module_name);if("add"===e.pageModel){let e=this.$store.getters.get_cur_node_info;this.pageData={parent_id:e.id,router_has_icon:"false"}}else if("view"===e.pageModel||"edit"===e.pageModel){let e=this.$store.getters.get_cur_node_info;this.pageData=e.value}return e}},async mounted(){this.mongodb_bool_type_code_list=await this.$setCodeList(this.mongodb_bool_type_code_list,"mongodb_bool_type")},methods:{async onSubmit(){let e=this;this.$refs.pageDataRef.validate(async t=>{if(t){let t=this.pageData;t.label=t.router_show_name,null!=await e.$insert(t,"OAMP_insert_sys_router_info")?(e.$message.success("新增信息成功"),e.$onClose(e.module_name,"pageDataRef",e.refresh_page_method)):e.$message.error("新增信息失败")}})},async onUpdate(){let e=this;this.$refs.pageDataRef.validate(async t=>{if(t){let t=this.pageData;null!=await e.$update(t,"OAMP_update_sys_router_info")?(e.$message.success("修改信息成功"),e.$onClose(e.module_name,"pageDataRef",e.refresh_page_method)):e.$message.error("修改信息失败")}})}}},r={render:function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("el-dialog",{attrs:{title:"节点信息",visible:e.pageInfo.isShow,"modal-append-to-body":!1,"close-on-click-modal":!1,center:!0,"lock-scroll":!1},on:{close:function(t){return e.onClose(e.module_name,"pageDataRef")}}},[a("el-form",{ref:"pageDataRef",attrs:{model:e.pageData,rules:e.pageDataRules,inline:!0,"label-width":"160px",size:"small"}},[a("el-form-item",{attrs:{label:"父节点id",prop:"parent_id"}},[a("el-input",{attrs:{disabled:""},model:{value:e.pageData.parent_id,callback:function(t){e.$set(e.pageData,"parent_id",t)},expression:"pageData.parent_id"}})],1),e._v(" "),a("el-form-item",{attrs:{label:"显示名称",prop:"label"}},[a("el-input",{attrs:{disabled:""},model:{value:e.pageData.label,callback:function(t){e.$set(e.pageData,"label",t)},expression:"pageData.label"}})],1),e._v(" "),a("el-form-item",{attrs:{label:"路由显示名称",prop:"router_show_name"}},[a("el-input",{model:{value:e.pageData.router_show_name,callback:function(t){e.$set(e.pageData,"router_show_name",t)},expression:"pageData.router_show_name"}})],1),e._v(" "),a("el-form-item",{attrs:{label:" 路由名称",prop:"router_name"}},[a("el-input",{model:{value:e.pageData.router_name,callback:function(t){e.$set(e.pageData,"router_name",t)},expression:"pageData.router_name"}})],1),e._v(" "),a("el-form-item",{attrs:{label:"路由路径",prop:"router_path"}},[a("el-input",{staticStyle:{width:"696px"},model:{value:e.pageData.router_path,callback:function(t){e.$set(e.pageData,"router_path",t)},expression:"pageData.router_path"}})],1),e._v(" "),a("el-form-item",{attrs:{label:"排序",prop:"order"}},[a("el-input",{attrs:{type:"number",step:"0.01"},model:{value:e.pageData.order,callback:function(t){e.$set(e.pageData,"order",t)},expression:"pageData.order"}})],1),e._v(" "),a("el-form-item",{attrs:{label:"是否有图标",prop:"router_has_icon"}},[a("el-select",{attrs:{placeholder:"请选择",clearable:""},model:{value:e.pageData.router_has_icon,callback:function(t){e.$set(e.pageData,"router_has_icon",t)},expression:"pageData.router_has_icon"}},e._l(e.mongodb_bool_type_code_list,function(e){return a("el-option",{key:e.codeId,attrs:{label:e.codeValue,value:e.codeId}})}),1)],1),e._v(" "),"true"===e.pageData.router_has_icon?a("el-form-item",{attrs:{label:"图标样式",prop:"router_icon_class"}},[a("el-input",{model:{value:e.pageData.router_icon_class,callback:function(t){e.$set(e.pageData,"router_icon_class",t)},expression:"pageData.router_icon_class"}})],1):e._e(),e._v(" "),"true"===e.pageData.router_has_icon?a("el-form-item",{attrs:{label:"图标大小",prop:"router_icon_class"}},[a("el-input",{model:{value:e.pageData.router_icon_size,callback:function(t){e.$set(e.pageData,"router_icon_size",t)},expression:"pageData.router_icon_size"}})],1):e._e(),e._v(" "),a("el-form-item",{attrs:{label:"备注",prop:"remark"}},[a("el-input",{staticStyle:{width:"696px"},attrs:{type:"textarea"},model:{value:e.pageData.remark,callback:function(t){e.$set(e.pageData,"remark",t)},expression:"pageData.remark"}})],1)],1),e._v(" "),a("div",{staticClass:"dialog-footer",attrs:{slot:"footer"},slot:"footer"},[a("el-button",{on:{click:function(t){return e.onClose(e.module_name,"pageDataRef")}}},[e._v("关 闭")]),e._v(" "),"add"===e.pageInfo.pageModel?a("el-button",{attrs:{type:"primary"},on:{click:e.onSubmit}},[e._v("确 定")]):"edit"===e.pageInfo.pageModel?a("el-button",{attrs:{type:"primary"},on:{click:e.onUpdate}},[e._v("更 新")]):e._e()],1)],1)},staticRenderFns:[]};var s={name:"sysFunctionInfoManage",components:{nodeInfo:a("VU/8")(o,r,!1,function(e){a("3kxu")},"data-v-305da528",null).exports},data(){return{module_name:"sysRouterInfoManageNode",refresh_page_method:"refresh_"+this.module_name,searchFormData:{order:"+router_path"},tableData:[],is_has_top_node:!0,is_selected_node:!1,selected_data:{},filterText:"",treeData:[],defaultProps:{children:"children",label:"label"}}},created(){this.$store.state.Apps.$on(this.refresh_page_method,()=>{this.refresh_node_info()})},async mounted(){this.search(),this.search_tree_data()},watch:{filterText(e){this.$refs.tree_ref.filter(e)}},methods:{async search(){this.selected_data.hasOwnProperty("value")&&(this.searchFormData.parent_id=this.selected_data.value.node_id);let e=await this.$search(this.searchFormData,"OAMP_search_sys_router_info_list");this.searchFormData.pageCount=e.pageCount,this.tableData=e.data},async search_tree_data(){let e=await this.$exec({},"OAMP_search_sys_router_tree_data");this.is_has_top_node=null!==e,this.treeData=null===e?[]:[e]},async add_sys_router_top_node_info(){null!=await this.$insert({},"OAMP_insert_sys_router_top_node_info")?(this.$message.success("新增顶级节点信息成功"),this.is_has_top_node=!0,this.search_tree_data()):this.$message.error("新增顶级节点信息失败")},renderContent:function(e,{node:t,data:a,store:o}){return e("span",[e("i",{attrs:{class:"iconfont "+a.value.router_icon_class}}),e("span","     "),e("span",t.label)])},filterNode:(e,t)=>!e||-1!==t.label.indexOf(e),node_click(e,t,a){this.is_selected_node=!0,this.selected_data=e,this.search()},add_node_info(){this.onAdd("sysRouterInfoManageNode"),this.$store.commit("change_cur_node_info",this.selected_data)},edit_node_info(){this.onEdit("sysRouterInfoManageNode",0,[this.selected_data]),this.$store.commit("change_cur_node_info",this.selected_data)},view_node_info(){this.onView("sysRouterInfoManageNode",0,[this.selected_data]),this.$store.commit("change_cur_node_info",this.selected_data)},async delete_node_info(){await this.$del(this.selected_data,"OAMP_delete_sys_router_info")&&(this.$message.success("删除路由节点信息成功"),this.is_selected_node=!1,this.selected_data={},this.search_tree_data())},refresh_node_info(){this.search_tree_data(),this.search()}}},l={render:function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("div",{staticClass:"v-container"},[a("el-breadcrumb",[a("el-breadcrumb-item",{attrs:{to:{name:"setting"}}},[e._v("设置")]),e._v(" "),a("el-breadcrumb-item",{attrs:{to:{name:"sysManage"}}},[e._v("系统管理")]),e._v(" "),a("el-breadcrumb-item",[e._v("系统功能信息管理")])],1),e._v(" "),a("hr"),e._v(" "),a("el-row",[a("el-col",{attrs:{span:10}},[a("el-col",{attrs:{offset:2,span:20}},[a("el-input",{attrs:{placeholder:"输入关键字进行过滤"},model:{value:e.filterText,callback:function(t){e.filterText=t},expression:"filterText"}})],1),e._v(" "),a("el-col",{staticStyle:{"text-align":"center",margin:"10px 30px"},attrs:{offset:2,span:20}},[!1===e.is_has_top_node?a("el-button",{attrs:{size:"small",type:"primary"},on:{click:e.add_sys_router_top_node_info}},[e._v("添加顶级节点")]):e._e(),e._v(" "),e.is_selected_node?a("el-button",{attrs:{size:"small",type:"primary"},on:{click:e.add_node_info}},[e._v("添加节点")]):e._e(),e._v(" "),e.is_selected_node?a("el-button",{attrs:{size:"small",type:"primary"},on:{click:e.edit_node_info}},[e._v("修改节点信息")]):e._e(),e._v(" "),e.is_selected_node?a("el-button",{attrs:{size:"small",type:"primary"},on:{click:e.view_node_info}},[e._v("查看节点信息")]):e._e(),e._v(" "),e.is_selected_node?a("el-button",{attrs:{size:"small",type:"primary"},on:{click:e.delete_node_info}},[e._v("删除节点")]):e._e(),e._v(" "),a("el-button",{attrs:{size:"small",type:"primary"},on:{click:e.refresh_node_info}},[e._v("刷新")])],1),e._v(" "),a("el-col",{attrs:{offset:3,span:18}},[a("div",{staticStyle:{margin:"0px 0px 5px"}},[e._v("当前选择节点:【"+e._s(e.selected_data.label)+"】")])]),e._v(" "),a("el-col",{attrs:{offset:2,span:20}},[a("div",{staticStyle:{height:"690px","overflow-y":"scroll","background-color":"#fff",padding:"10px"}},[a("el-tree",{ref:"tree_ref",attrs:{draggable:"",data:e.treeData,props:e.defaultProps,"default-expand-all":"","filter-node-method":e.filterNode,"render-content":e.renderContent},on:{"node-click":e.node_click}})],1)])],1),e._v(" "),a("el-col",{attrs:{span:14}},[a("el-table",{attrs:{data:e.tableData,border:!0,stripe:!0,size:"mini",height:e.getTableHeight(32)}},[a("el-table-column",{attrs:{fixed:"",type:"index",index:e.onIndexMethod(),label:"序号",width:"60"}}),e._v(" "),a("el-table-column",{attrs:{prop:"createTime",label:"创建时间",width:"156"}}),e._v(" "),a("el-table-column",{attrs:{"show-overflow-tooltip":!0,prop:"router_show_name",label:"显示名称",width:"110"}}),e._v(" "),a("el-table-column",{attrs:{"show-overflow-tooltip":!0,prop:"router_name",label:"路由名称",width:"110"}}),e._v(" "),a("el-table-column",{attrs:{"show-overflow-tooltip":!0,prop:"router_path",label:"路由路径"}}),e._v(" "),a("el-table-column",{attrs:{label:"图标",width:"50"},scopedSlots:e._u([{key:"default",fn:function(e){return[a("i",{class:"iconfont "+e.row.router_icon_class})]}}])}),e._v(" "),a("el-table-column",{attrs:{prop:"router_icon_size",label:"尺寸",width:"50"}}),e._v(" "),a("el-table-column",{attrs:{"show-overflow-tooltip":!0,prop:"router_icon_class",label:"图标样式",width:"180"}})],1)],1)],1),e._v(" "),a("nodeInfo")],1)},staticRenderFns:[]};var n=a("VU/8")(s,l,!1,function(e){a("lBVQ")},"data-v-d858e79a",null);t.default=n.exports},lBVQ:function(e,t){}});
//# sourceMappingURL=20.cea44eef619562f8977f.js.map