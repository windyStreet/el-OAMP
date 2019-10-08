webpackJsonp([1],{"+zye":function(e,t){},"1WLe":function(e,t){},"5DL6":function(e,t,o){"use strict";Object.defineProperty(t,"__esModule",{value:!0});var a={name:"projectRemarkUpdateInfo",data(){return{module_name:"projectRemarkUpdateInfo",project_code_list:null,project_opt_type_code_list:null,exec_state_code_list:null,searchFormData:{project_id:this.$store.getters.get_authority_project_id,project_opt_type_code_id:"2",pageNum:1,pageSize:11,pageCount:1,order:"-createTime"},tableData:[]}},async mounted(){this.project_code_list=await this.$getProjectCodeInfo(),this.project_opt_type_code_list=await this.$setCodeList(this.project_opt_type_code_list,"project_opt_type"),this.exec_state_code_list=await this.$setCodeList(this.exec_state_code_list,"exec_state"),this.search()},computed:{pageInfo(){return this.$setPageInfo(this.module_name)}},methods:{handleSizeChange(e){this.searchFormData.pageSize=e,this.search()},handleCurrentChange(e){this.searchFormData.pageNum=e,this.search()},onReset(){this.$refs.searchFormRef.resetFields(),this.search()},onSearch(){this.searchFormData.pageNum=1,this.search()},async search(){let e=this.searchFormData,t=await this.$search(e,"OAMP_search_project_opt_record_info_list");this.searchFormData.pageCount=t.pageCount,this.tableData=t.data},format_project(e,t,o){return this.$formatCodeValue(e,this.project_code_list,t.property,"_id","project_name")},format_project_opt_type(e,t,o){return this.$formatCodeValue(e,this.project_opt_type_code_list,"project_opt_type_code_id")},format_is_opt_success:(e,t,o)=>"1"===e.is_opt_success?"成功":"0"===e.is_opt_success?"失败":"暂无结果",format_exec_state(e,t,o){return this.$formatCodeValue(e,this.exec_state_code_list,"exec_state_code_id")},remark_update(e,t){let o=t[e];this.$exec(o,"OAMP_project_remark_update")},ramark_cancel(e,t){let o=t[e],a=this.$exec(o,"OAMP_project_remark_cancel");"1"===a.is_success?t[e]=a.data:this.$message.error("项目标记取消失败!")}}},s={render:function(){var e=this,t=e.$createElement,o=e._self._c||t;return o("el-dialog",{attrs:{title:"标记更新列表信息",width:"1200px",visible:e.pageInfo.isShow,"modal-append-to-body":!1,"close-on-click-modal":!1,center:!0,"lock-scroll":!1},on:{close:function(t){return e.onClose(e.module_name)}}},[o("el-form",{ref:"searchFormRef",attrs:{inline:!0,model:e.searchFormData,size:"mini"}},[o("el-form-item",{attrs:{label:"创建时间",prop:"createTime"}},[o("el-date-picker",{attrs:{type:"daterange","range-separator":"至","start-placeholder":"开始日期","end-placeholder":"结束日期"},model:{value:e.searchFormData.createTime,callback:function(t){e.$set(e.searchFormData,"createTime",t)},expression:"searchFormData.createTime"}})],1),e._v(" "),o("div",{staticClass:"v-center"},[o("div",{staticClass:"v-inline"},[o("el-button",{attrs:{size:"mini",type:"primary"},on:{click:e.onSearch}},[o("i",{staticClass:"iconfont icon-chaxun"}),e._v(" 查询")]),e._v(" "),o("el-button",{attrs:{size:"mini",type:"primary"},on:{click:e.onReset}},[o("i",{staticClass:"iconfont icon-chongzhi"}),e._v(" 重置")]),e._v(" "),o("el-button",{attrs:{size:"mini",type:"primary"},on:{click:function(t){return e.onClose(e.module_name)}}},[o("i",{staticClass:"iconfont icon-guanbi"}),e._v(" 关闭")])],1)])],1),e._v(" "),o("hr"),e._v(" "),o("el-table",{attrs:{data:e.tableData,border:!0,stripe:!0,size:"mini",height:e.getTableHeight(360)}},[o("el-table-column",{attrs:{fixed:"",type:"index",index:e.onIndexMethod(e.searchFormData.pageNum,e.searchFormData.pageSize),label:"序号",width:"60"}}),e._v(" "),o("el-table-column",{attrs:{prop:"createTime",label:"创建时间",width:"160"}}),e._v(" "),o("el-table-column",{attrs:{width:"156","show-overflow-tooltip":!0,prop:"project_id",label:"项目名称",formatter:e.format_project}}),e._v(" "),o("el-table-column",{attrs:{prop:"project_opt_type_code_id",label:"操作类型",width:"80",formatter:e.format_project_opt_type}}),e._v(" "),o("el-table-column",{attrs:{prop:"project_opt_version",label:"操作版本",width:"80"}}),e._v(" "),o("el-table-column",{attrs:{prop:"is_opt_success",label:"操作结果",width:"80",formatter:e.format_is_opt_success}}),e._v(" "),o("el-table-column",{attrs:{prop:"project_opt_last_version",label:"上个版本",width:"80"}}),e._v(" "),o("el-table-column",{attrs:{prop:"exec_state_code_id",label:"远程执行状态",formatter:e.format_exec_state,width:"100"}}),e._v(" "),o("el-table-column",{attrs:{prop:"project_opt_summary",label:"操作描述","show-overflow-tooltip":!0}}),e._v(" "),o("el-table-column",{attrs:{fixed:"right",label:"操作",width:"200"},scopedSlots:e._u([{key:"default",fn:function(t){return["1"===t.row.is_opt_success?o("el-col",{attrs:{span:12}},[o("el-button",{attrs:{type:"primary",size:"mini"},on:{click:function(o){return e.remark_update(t.$index,e.tableData)}}},[e._v("标记更新")])],1):e._e(),e._v(" "),"1"===t.row.is_opt_success?o("el-col",{attrs:{span:12}},[o("el-button",{attrs:{type:"primary",size:"mini"},on:{click:function(o){return e.ramark_cancel(t.$index,e.tableData)}}},[e._v("标记取消")])],1):e._e()]}}])})],1),e._v(" "),o("el-paginations",{attrs:{"current-page":e.searchFormData.pageNum,"page-size":e.searchFormData.pageSize,total:e.searchFormData.pageCount,"page-sizes":[11,20,50,100],layout:"total, sizes, prev, pager, next, jumper"},on:{"size-change":e.handleSizeChange,"current-change":e.handleCurrentChange}})],1)},staticRenderFns:[]};var r=o("VU/8")(a,s,!1,function(e){o("+zye")},"data-v-30ae01a1",null).exports,i={name:"projectRollBackInfo",data:()=>({module_name:"projectRollBackInfo",project_code_list:null,searchFormData:{pageNum:1,pageSize:11,pageCount:1,order:"_createTime"},tableData:[]}),async mounted(){this.project_code_list=await this.$getProjectCodeInfo(),this.search()},computed:{pageInfo(){return this.$setPageInfo(this.module_name)}},methods:{handleSizeChange(e){this.searchFormData.pageSize=e,this.search()},handleCurrentChange(e){this.searchFormData.pageNum=e,this.search()},onReset(){this.$refs.searchFormRef.resetFields(),this.search()},onSearch(){this.searchFormData.pageNum=1,this.search()},async search(){let e=this.searchFormData,t=await this.$search(e,"OAMP_search_project_opt_record_info_list");this.searchFormData.pageCount=t.pageCount,this.tableData=t.data},format_project(e,t,o){return this.$formatCodeValue(e,this.project_code_list,t.property,"_id","project_name")}}},c={render:function(){var e=this,t=e.$createElement,o=e._self._c||t;return o("el-dialog",{attrs:{title:"标记更新列表信息",visible:e.pageInfo.isShow,"modal-append-to-body":!1,"close-on-click-modal":!1,center:!0,"lock-scroll":!1},on:{close:function(t){return e.onClose(e.module_name)}}},[o("el-form",{ref:"searchFormRef",attrs:{inline:!0,model:e.searchFormData,size:"mini"}},[o("el-form-item",{attrs:{label:"创建时间",prop:"createTime"}},[o("el-date-picker",{attrs:{type:"daterange","range-separator":"至","start-placeholder":"开始日期","end-placeholder":"结束日期"},model:{value:e.searchFormData.createTime,callback:function(t){e.$set(e.searchFormData,"createTime",t)},expression:"searchFormData.createTime"}})],1),e._v(" "),o("div",{staticClass:"v-center"},[o("div",{staticClass:"v-inline"},[o("el-button",{attrs:{size:"mini",type:"primary"},on:{click:e.onSearch}},[o("i",{staticClass:"iconfont icon-chaxun"}),e._v(" 查询")]),e._v(" "),o("el-button",{attrs:{size:"mini",type:"primary"},on:{click:e.onReset}},[o("i",{staticClass:"iconfont icon-chongzhi"}),e._v(" 重置")]),e._v(" "),o("el-button",{attrs:{size:"mini",type:"primary"},on:{click:function(t){return e.onClose(e.module_name)}}},[o("i",{staticClass:"iconfont icon-guanbi"}),e._v(" 关闭")])],1)])],1),e._v(" "),o("hr"),e._v(" "),o("el-table",{attrs:{data:e.tableData,border:!0,stripe:!0,size:"mini",height:e.getTableHeight(360)}},[o("el-table-column",{attrs:{fixed:"",type:"index",index:e.onIndexMethod(e.searchFormData.pageNum,e.searchFormData.pageSize),label:"序号",width:"60"}}),e._v(" "),o("el-table-column",{attrs:{prop:"createTime",label:"创建时间",width:"160"}}),e._v(" "),o("el-table-column",{attrs:{width:"156","show-overflow-tooltip":!0,prop:"project_id",label:"项目名称",formatter:e.format_project}}),e._v(" "),o("el-table-column",{attrs:{fixed:"right",label:"操作",width:"120"},scopedSlots:e._u([{key:"default",fn:function(t){return[o("el-col",{attrs:{span:24}},[o("el-col",{attrs:{span:11}},[o("el-button",{attrs:{type:"danger",size:"mini"}},[e._v("容器已被关联")])],1)],1)]}}])})],1),e._v(" "),o("el-pagination",{attrs:{"current-page":e.searchFormData.pageNum,"page-size":e.searchFormData.pageSize,total:e.searchFormData.pageCount,"page-sizes":[11,20,50,100],layout:"total, sizes, prev, pager, next, jumper"},on:{"size-change":e.handleSizeChange,"current-change":e.handleCurrentChange}})],1)},staticRenderFns:[]};var _={name:"projectUpdateInfo",components:{projectRemarkUpdateInfo:r,projectRollBackInfo:o("VU/8")(i,c,!1,function(e){o("T8vM")},"data-v-8db83b36",null).exports},data:()=>({libJarTableData:[],ResourceLibTableData:[],staticFileDirPathTableData:[],updateResTableData:[],selectedLibRes:[],selectedResourceLibRes:[],selectedStaticFileDirRes:[],project_opt_type_code_id:"-1",update_info:{project_opt_version:"",project_opt_summary:"",project_opt_last_version:""},cur_project_id:"",resource_type_code_list:null,local_update_res_path:"",updateRules:{project_opt_version:[{required:!0,message:"请输入版本号",trigger:"blur"}]},is_exec_loading:!1,project_info:null,update_conf_info:null}),async mounted(){if(this.cur_project_id=this.$store.getters.get_authority_project_id,null!=this.cur_project_id&&""!==this.cur_project_id){this.resource_type_code_list=await this.$setCodeList(this.resource_type_code_list,"resource_type");let{data:e}=await this.$search({project_id:this.cur_project_id},"OAMP_search_project_update_conf_info_list");if(null!=e){let t=e[0];this.update_conf_info=t,this.local_update_res_path=t.update_path,await this.initPage()}else this.$message.warning("未配置项目更新信息")}else this.$message.error("页面错误，未选择当前项目")},methods:{async initPage(){let e={path:this.local_update_res_path,isShowFile:"1"},t=await this.$exec(e,"OAMP_get_lib_res_info");null!=t&&(this.libJarTableData=t.data);let o={path:this.local_update_res_path,isShowFile:"1"},a=await this.$exec(o,"OAMP_get_ResourceLib_res_info");null!=a&&(this.ResourceLibTableData=a.data);let s={path:this.local_update_res_path,isShowFile:"0"},r=await this.$exec(s,"OAMP_get_static_res_info");null!=r&&(this.staticFileDirPathTableData=r.data),this.search_project_info()},async search_project_info(){if(null!=this.cur_project_id&&""!==this.cur_project_id){let e={project_id:this.cur_project_id},{data:t}=await this.$search(e,"OAMP_search_project_info_by_id");this.project_info=t}},ibResChange(e){this.selectedLibRes=e,this.updateResTableData=[].concat(this.selectedLibRes).concat(this.selectedResourceLibRes).concat(this.selectedStaticFileDirRes)},resourceLibResChange(e){this.selectedResourceLibRes=e,this.updateResTableData=[].concat(this.selectedLibRes).concat(this.selectedResourceLibRes).concat(this.selectedStaticFileDirRes)},staticFileDirResChange(e){this.selectedStaticFileDirRes=e,this.updateResTableData=[].concat(this.selectedLibRes).concat(this.selectedResourceLibRes).concat(this.selectedStaticFileDirRes)},libResClick(e,t,o,a){this.$refs.libJarTableRef.toggleRowSelection(e)},resourceLibResClick(e,t,o,a){this.$refs.ResourceLibTableRef.toggleRowSelection(e)},staticFileDirResClick(e,t,o,a){this.$refs.staticFileDirPathTableRef.toggleRowSelection(e)},format_resource_type(e,t,o){return this.$formatCodeValue(e,this.resource_type_code_list,t.property)},async project_modify_full_res(){this.update_conf_info.update_ex_resource=[{libRes:this.selectedLibRes},{ResourceLibRes:this.selectedResourceLibRes},{staticFileRes:this.selectedStaticFileDirRes}];let e=await this.$update(this.update_conf_info,"OAMP_update_project_update_conf_info");this.is_exec_loading=!1,null!=e?this.$message.success("修改全量资源信息成功"):this.$message.error("修改全量资源信息失败")},async project_restart(){let e={project_id:this.cur_project_id,project_opt_summary:this.update_info.project_opt_summary,project_opt_version:this.update_info.project_opt_version},t=await this.$exec(e,"OMAP_project_restart");this.is_exec_loading=!1,null!=t&&"1"===t.is_success?this.$message.success("项目重启操作成功"):"0"===t.is_success&&this.$message.warning("项目重启操作异常")},async project_remark_version(){let e={project_id:this.cur_project_id,libRes:this.selectedLibRes,resourceLibRes:this.selectedResourceLibRes,staticFileRes:this.selectedStaticFileDirRes,project_opt_version:this.update_info.project_opt_version,project_opt_summary:this.update_info.project_opt_summary,project_opt_last_version:this.update_info.project_opt_last_version},t=await this.$exec(e,"OAMP_project_remark_version");this.is_exec_loading=!1,null!=t&&"1"===t.is_success?(this.$message.success("标记项目成功"),await this.search_project_info(),this.project_opt_type_change(this.project_opt_type_code_id)):this.$message.warning("项目标记异常，请重试或者联系运维人员")},async project_static_file_update(){let e={project_id:this.cur_project_id,libRes:this.selectedLibRes,resourceLibRes:this.selectedResourceLibRes,staticFileRes:this.selectedStaticFileDirRes,project_opt_version:this.update_info.project_opt_version,project_opt_summary:this.update_info.project_opt_summary,project_opt_last_version:this.update_info.project_opt_last_version},t=await this.$exec(e,"OAMP_project_static_file_update");this.is_exec_loading=!1,null!=t&&"1"===t.is_success?this.$message.success("项目资源替换操作成功"):"0"===t.is_success&&this.$message.warning("项目资源替换操作异常")},async project_full_update(){let e={project_id:this.cur_project_id,libRes:this.selectedLibRes,resourceLibRes:this.selectedResourceLibRes,staticFileRes:this.selectedStaticFileDirRes,project_opt_version:this.update_info.project_opt_version,project_opt_summary:this.update_info.project_opt_summary,project_opt_last_version:this.update_info.project_opt_last_version},t=await this.$exec(e,"OAMP_project_full_update");this.is_exec_loading=!1,null!=t&&"1"===t.is_success?this.$message.success("项目全量更新操作成功"):"0"===t.is_success&&this.$message.warning("项目全量更新操作异常")},async project_increase_update(){let e={project_id:this.cur_project_id,libRes:this.selectedLibRes,resourceLibRes:this.selectedResourceLibRes,staticFileRes:this.selectedStaticFileDirRes,project_opt_version:this.update_info.project_opt_version,project_opt_summary:this.update_info.project_opt_summary,project_opt_last_version:this.update_info.project_opt_last_version},t=await this.$exec(e,"OAMP_project_increase_update");this.is_exec_loading=!1,null!=t&&"1"===t.is_success?this.$message.success("项目增量更新操作成功"):"0"===t.is_success&&this.$message.warning("项目增量更新操作异常")},project_opt_notify_info(e,t,o){if(o){let o="<i>"+e+"成功服务器共计<strong><i>"+t.success_count+"</i></strong>个<br>成功ip为:<br>";return t.success_ips.forEach(e=>{o+="[<strong><i>"+e+"</i></strong>]<br>"}),o+="</i>"}{let o="<strong><i>"+e+"服务器总数"+t.exec_count+"个</i></strong><br>";return o+="<i>"+e+"成功服务器共计<strong><i>"+t.success_count+"</i></strong>个<br>成功ip为:<br>",t.success_ips.forEach(e=>{o+="[<strong><i>"+e+"</i></strong>]<br>"}),o+="</i>",o+="<i>"+e+"失败服务器共计<strong><i>"+t.failed_count+"</i></strong>个<br>失败ip为:<br>",t.failed_ips.forEach(e=>{o+="[<strong><i>"+e+"</i></strong>]<br>"}),o+="</i>"}},add_version(e){let t=e.toString().split(".");if(t.length<=1)return parseInt(t[0]).toString()+".001";{let e="000".concat((parseInt(t[1])+1).toString());return t[0]+"."+e.substring(e.length-3,e.length).toString()}},project_opt_type_change(e){switch(this.update_info.project_opt_summary="",parseInt(e)){case 1:this.update_info.project_opt_version=this.project_info.project_version;break;case 2:case 3:this.update_info.project_opt_version=this.add_version(this.project_info.project_version),this.update_info.project_opt_last_version=this.project_info.project_version;break;case 4:this.onAdd("projectRemarkUpdateInfo");break;case 5:this.update_info.project_opt_version=parseInt(this.project_info.project_version)+1,this.update_info.project_opt_last_version=this.project_info.project_version;break;case 6:this.update_info.project_opt_version=this.add_version(this.project_info.project_version),this.update_info.project_opt_last_version=this.project_info.project_version;break;case 7:this.onAdd("projectRollBackInfo")}},project_opt_exec(){this.$refs.project_opt_form.validate(e=>{if(e)switch(this.is_exec_loading=!0,parseInt(this.project_opt_type_code_id)){case 0:this.project_modify_full_res();break;case 1:this.project_restart();break;case 2:this.project_remark_version();break;case 3:this.project_static_file_update();break;case 4:break;case 5:this.project_full_update();break;case 6:this.project_increase_update()}})}}},l={render:function(){var e=this,t=e.$createElement,o=e._self._c||t;return o("div",{staticStyle:{"padding-right":"10px"}},[o("el-row",{attrs:{gutter:10}},[o("el-col",{attrs:{span:5}},[o("div",{staticClass:"cont",style:"height:"+e.getAutoHeight(144)+";"},[o("el-table",{ref:"libJarTableRef",attrs:{border:!0,stripe:!0,size:"mini",height:e.getTableHeight(70),data:e.libJarTableData},on:{"selection-change":e.ibResChange,"cell-click":e.libResClick}},[o("el-table-column",{attrs:{label:"选择服务端资源"}},[o("el-table-column",{attrs:{type:"selection",width:"55"}}),e._v(" "),o("el-table-column",{attrs:{prop:"res_name",label:"资源名称","show-overflow-tooltip":""}})],1)],1)],1)]),e._v(" "),o("el-col",{attrs:{span:5}},[o("div",{staticClass:"cont",style:"height:"+e.getAutoHeight(144)+";"},[o("el-table",{ref:"ResourceLibTableRef",attrs:{border:!0,stripe:!0,size:"mini",height:e.getTableHeight(330),data:e.ResourceLibTableData},on:{"selection-change":e.resourceLibResChange,"cell-click":e.resourceLibResClick}},[o("el-table-column",{attrs:{label:"选择前端资源"}},[o("el-table-column",{attrs:{type:"selection",width:"55"}}),e._v(" "),o("el-table-column",{attrs:{prop:"res_name",label:"资源名称","show-overflow-tooltip":""}})],1)],1),e._v(" "),o("hr"),e._v(" "),o("el-table",{ref:"staticFileDirPathTableRef",attrs:{border:!0,stripe:!0,size:"mini",height:e.getTableHeight(620),data:e.staticFileDirPathTableData},on:{"selection-change":e.staticFileDirResChange,"cell-click":e.staticFileDirResClick}},[o("el-table-column",{attrs:{label:"选择静态资源"}},[o("el-table-column",{attrs:{type:"selection",width:"55"}}),e._v(" "),o("el-table-column",{attrs:{prop:"res_name",label:"资源名称","show-overflow-tooltip":""}})],1)],1)],1)]),e._v(" "),o("el-col",{attrs:{span:14}},[o("div",{staticClass:"cont",style:"height:"+e.getAutoHeight(144)+";"},[o("el-table",{attrs:{border:!0,stripe:!0,size:"mini",height:e.getTableHeight(500),data:e.updateResTableData}},[o("el-table-column",{attrs:{label:"已选择更新内容"}},[o("el-table-column",{attrs:{fixed:"",type:"index",index:e.onIndexMethod(),label:"序号",width:"60"}}),e._v(" "),o("el-table-column",{attrs:{prop:"res_name",label:"资源名称","show-overflow-tooltip":"",width:"260"}}),e._v(" "),o("el-table-column",{attrs:{prop:"resource_type_code_id",formatter:e.format_resource_type,label:"资源类型",width:"80"}}),e._v(" "),o("el-table-column",{attrs:{prop:"res_path",label:"资源路径","show-overflow-tooltip":""}})],1)],1),e._v(" "),o("hr"),e._v(" "),o("el-row",[o("el-radio-group",{attrs:{fill:"#e6a23c"},on:{change:e.project_opt_type_change},model:{value:e.project_opt_type_code_id,callback:function(t){e.project_opt_type_code_id=t},expression:"project_opt_type_code_id"}},[o("el-radio-button",{attrs:{label:"0"}},[e._v("修改全量资源")]),e._v(" "),o("el-radio-button",{attrs:{label:"1"}},[e._v("重启项目")]),e._v(" "),o("el-radio-button",{attrs:{label:"2"}},[e._v("标记项目")]),e._v(" "),o("el-radio-button",{attrs:{label:"3"}},[e._v("资源替换")]),e._v(" "),o("el-radio-button",{attrs:{label:"4"}},[e._v("标记更新")]),e._v(" "),o("el-radio-button",{attrs:{label:"5"}},[e._v("全量更新")]),e._v(" "),o("el-radio-button",{attrs:{label:"6"}},[e._v("增量更新")]),e._v(" "),o("el-radio-button",{attrs:{disabled:"",label:"7"}},[e._v("回滚项目")])],1)],1),e._v(" "),o("hr"),e._v(" "),o("div",{staticClass:"form_update"},[o("el-form",{ref:"project_opt_form",attrs:{"label-width":"110px",model:e.update_info,rules:e.updateRules}},["1"===e.project_opt_type_code_id?o("el-row",[o("el-form-item",{attrs:{label:"当前版本号:",prop:"project_opt_version"}},[o("el-input",{attrs:{disabled:""},model:{value:e.update_info.project_opt_version,callback:function(t){e.$set(e.update_info,"project_opt_version",t)},expression:"update_info.project_opt_version"}})],1),e._v(" "),o("el-form-item",{attrs:{label:"重启原因:",prop:"project_opt_summary"}},[o("el-input",{attrs:{type:"textarea"},model:{value:e.update_info.project_opt_summary,callback:function(t){e.$set(e.update_info,"project_opt_summary",t)},expression:"update_info.project_opt_summary"}})],1)],1):e._e(),e._v(" "),"2"===e.project_opt_type_code_id?o("el-row",[o("el-form-item",{attrs:{label:"更新版号:",prop:"project_opt_version"}},[o("el-input",{attrs:{type:"number",step:"0.001",placeholder:"请输入更新版号"},model:{value:e.update_info.project_opt_version,callback:function(t){e.$set(e.update_info,"project_opt_version",t)},expression:"update_info.project_opt_version"}})],1),e._v(" "),o("el-form-item",{attrs:{label:"上个版号:",prop:"project_opt_last_version"}},[o("el-input",{attrs:{disabled:""},model:{value:e.update_info.project_opt_last_version,callback:function(t){e.$set(e.update_info,"project_opt_last_version",t)},expression:"update_info.project_opt_last_version"}})],1),e._v(" "),o("el-form-item",{attrs:{label:"更新内容:",prop:"project_opt_summary"}},[o("el-input",{attrs:{type:"textarea",placeholder:"请输入更新内容"},model:{value:e.update_info.project_opt_summary,callback:function(t){e.$set(e.update_info,"project_opt_summary",t)},expression:"update_info.project_opt_summary"}})],1)],1):e._e(),e._v(" "),"3"===e.project_opt_type_code_id?o("el-row",[o("el-form-item",{attrs:{label:"更新版号:",prop:"project_opt_version"}},[o("el-input",{attrs:{disabled:""},model:{value:e.update_info.project_opt_version,callback:function(t){e.$set(e.update_info,"project_opt_version",t)},expression:"update_info.project_opt_version"}})],1),e._v(" "),o("el-form-item",{attrs:{label:"上个版号:",prop:"project_opt_last_version"}},[o("el-input",{attrs:{disabled:""},model:{value:e.update_info.project_opt_last_version,callback:function(t){e.$set(e.update_info,"project_opt_last_version",t)},expression:"update_info.project_opt_last_version"}})],1),e._v(" "),o("el-form-item",{attrs:{label:"更新内容:",prop:"project_opt_summary"}},[o("el-input",{attrs:{type:"textarea",placeholder:"请输入更新内容"},model:{value:e.update_info.project_opt_summary,callback:function(t){e.$set(e.update_info,"project_opt_summary",t)},expression:"update_info.project_opt_summary"}})],1)],1):e._e(),e._v(" "),"5"===e.project_opt_type_code_id?o("el-row",[o("el-form-item",{attrs:{label:"更新版号:",prop:"project_opt_version"}},[o("el-input",{attrs:{type:"number",step:"0.001",placeholder:"请输入更新版号"},model:{value:e.update_info.project_opt_version,callback:function(t){e.$set(e.update_info,"project_opt_version",t)},expression:"update_info.project_opt_version"}})],1),e._v(" "),o("el-form-item",{attrs:{label:"上个版号:",prop:"project_opt_last_version"}},[o("el-input",{attrs:{disabled:""},model:{value:e.update_info.project_opt_last_version,callback:function(t){e.$set(e.update_info,"project_opt_last_version",t)},expression:"update_info.project_opt_last_version"}})],1),e._v(" "),o("el-form-item",{attrs:{label:"更新内容:",prop:"project_opt_summary"}},[o("el-input",{attrs:{type:"textarea",placeholder:"请输入更新内容"},model:{value:e.update_info.project_opt_summary,callback:function(t){e.$set(e.update_info,"project_opt_summary",t)},expression:"update_info.project_opt_summary"}})],1)],1):e._e(),e._v(" "),"6"===e.project_opt_type_code_id?o("el-row",[o("el-form-item",{attrs:{label:"更新版号:",prop:"project_opt_version"}},[o("el-input",{attrs:{disabled:""},model:{value:e.update_info.project_opt_version,callback:function(t){e.$set(e.update_info,"project_opt_version",t)},expression:"update_info.project_opt_version"}})],1),e._v(" "),o("el-form-item",{attrs:{label:"上个版号:",prop:"project_opt_last_version"}},[o("el-input",{attrs:{disabled:""},model:{value:e.update_info.project_opt_last_version,callback:function(t){e.$set(e.update_info,"project_opt_last_version",t)},expression:"update_info.project_opt_last_version"}})],1),e._v(" "),o("el-form-item",{attrs:{label:"更新内容:",prop:"project_opt_summary"}},[o("el-input",{attrs:{type:"textarea",placeholder:"请输入更新内容"},model:{value:e.update_info.project_opt_summary,callback:function(t){e.$set(e.update_info,"project_opt_summary",t)},expression:"update_info.project_opt_summary"}})],1)],1):e._e()],1)],1),e._v(" "),o("hr"),e._v(" "),o("el-row",{staticClass:"v-center"},[null!==e.project_info&&"-1"!==e.project_opt_type_code_id&&"4"!==e.project_opt_type_code_id?o("el-button",{attrs:{type:"warning",loading:e.is_exec_loading},on:{click:function(t){return e.project_opt_exec()}}},[e._v("执行")]):o("el-button",{attrs:{disabled:"",type:"warning"}},[e._v("执行")])],1)],1)])],1),e._v(" "),o("projectRemarkUpdateInfo"),e._v(" "),o("projectRollBackInfo")],1)},staticRenderFns:[]};var p={name:"projectUpdate",components:{projectUpdateInfo:o("VU/8")(_,l,!1,function(e){o("1WLe")},"data-v-71534c2f",null).exports}},n={render:function(){var e=this.$createElement,t=this._self._c||e;return t("div",{staticClass:"v-container"},[t("el-breadcrumb",[t("el-breadcrumb-item",{attrs:{to:{name:"setting"}}},[this._v("设置")]),this._v(" "),t("el-breadcrumb-item",{attrs:{to:{name:"projectManage"}}},[this._v("项目管理")]),this._v(" "),t("el-breadcrumb-item",[this._v("项目更新")])],1),this._v(" "),t("hr"),this._v(" "),t("projectUpdateInfo")],1)},staticRenderFns:[]};var d=o("VU/8")(p,n,!1,function(e){o("TogM")},"data-v-5004e6e5",null);t.default=d.exports},T8vM:function(e,t){},TogM:function(e,t){}});
//# sourceMappingURL=1.9ef1dac09e589da1bcca.js.map