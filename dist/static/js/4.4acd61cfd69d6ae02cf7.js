webpackJsonp([4],{"2LZq":function(t,e){},"6tni":function(t,e){},J6AL:function(t,e,a){"use strict";Object.defineProperty(e,"__esModule",{value:!0});var o={name:"cdnUploadRecordList",data(){return{module_name:"cdnUpload",refresh_page_method:"refresh_"+this.module_name,upload_project_info_list:null,to_cdn_state_list:null,upload_state_list:null,upload_mode_type_list:null,reliability_state_code_list:null,searchFormData:{fileName:"",upload_project_id:"",to_cdn_state_code_id:"",creator:"",createTime:"",pageNum:1,pageSize:16,pageCount:1,order:"-createTime"},tableData:[]}},created(){this.$store.state.Apps.$on(this.refresh_page_method,()=>{this.onSearch()})},async mounted(){this.upload_mode_type_list=await this.$setCodeList(this.upload_mode_type_list,"upload_mode_type"),this.reliability_state_code_list=await this.$setCodeList(this.reliability_state_code_list,"reliability_state"),this.set_to_cdn_state_code(),this.set_upload_state_code(),this.set_upload_project_info_list(),this.onSearch()},methods:{handleSizeChange(t){this.searchFormData.pageSize=t,this.onSearch()},handleCurrentChange(t){this.searchFormData.pageNum=t,this.onSearch()},onReset(){this.$refs.searchFormRef.resetFields(),this.onSearch()},async set_to_cdn_state_code(){this.to_cdn_state_list||(this.to_cdn_state_list=await this.$getCodeValuesByCode("to_cdn_state"))},async set_upload_state_code(){this.upload_state_list||(this.upload_state_list=await this.$getCodeValuesByCode("upload_state"))},async set_upload_project_info_list(){this.upload_project_info_list||(this.upload_project_info_list=await this.$getProjectCodeInfo())},format_to_cdn_state(t,e,a){if(this.to_cdn_state_list&&this.to_cdn_state_list.length>0){let e=this.to_cdn_state_list.filter(e=>e.codeId===t.to_cdn_state_code_id);if(null!=e&&e.length>0)return e[0].codeValue}},format_upload_state(t,e,a){return this.$formatCodeValue(t,this.upload_state_list,e.property)},format_upload_mode_type(t,e,a){return this.$formatCodeValue(t,this.upload_mode_type_list,e.property)},formatIsToCDN:(t,e,a)=>!0===t.isToCdn?"是":"否",format_upload_project(t,e,a){return this.$formatCodeValue(t,this.upload_project_info_list,e.property,"_id","project_name")},format_reliability_state_style(t,e){let a=t[e];return"90"===a?"set-danger-4":"80"===a?"set-danger-3":"70"===a?"set-danger-2":"50"===a?"set-danger-1":"0"===a?"set-danger-0":"set-info"},format_reliability_state(t,e,a){return this.$formatCodeValue(t,this.reliability_state_code_list,"reliability_state_code_id")},async r_getUploadInfoList(t){let e=new this.$http,{data:a}=await e.post(t,"OAMP_search_upload_list");this.searchFormData.pageCount=a.pageCount,this.tableData=a.data},async r_retransmission(t){let e=new this.$http,{data:a}=await e.post(t,"OAMP_retransmission");return a},downloadFile(t,e){},retransmission(t,e){this.tableData[t].to_cdn_state_code_id=0,e[t].to_cdn_state_code_id=0;let a=this.r_retransmission(e[t]);this.to_cdn_state_code_id=this.format_upload_state(e[t],null,null),null!=a&&"true"===a.get("is_success")?this.$message.success("转移文件任务重新启动成功"):this.$message.error("转移文件任务重新启动失败")},onRefresh(){this.onSearch()},onSearch(){let t=this.searchFormData;this.r_getUploadInfoList(t)}}},l={render:function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",{staticStyle:{"padding-top":"6px"}},[a("el-form",{ref:"searchFormRef",attrs:{inline:!0,model:t.searchFormData,size:"mini"}},[a("el-form-item",{attrs:{label:"文件名称",prop:"fileName"}},[a("el-input",{attrs:{placeholder:"文件名称"},model:{value:t.searchFormData.fileName,callback:function(e){t.$set(t.searchFormData,"fileName",e)},expression:"searchFormData.fileName"}})],1),t._v(" "),a("el-form-item",{attrs:{label:"项目名称",prop:"upload_project_id"}},[a("el-select",{attrs:{placeholder:"请选项目名称",clearable:""},model:{value:t.searchFormData.upload_project_id,callback:function(e){t.$set(t.searchFormData,"upload_project_id",e)},expression:"searchFormData.upload_project_id"}},t._l(t.upload_project_info_list,function(t){return a("el-option",{key:t.project,attrs:{label:t.project_name,value:t._id}})}),1)],1),t._v(" "),a("el-form-item",{attrs:{label:"上传时间",prop:"createTime"}},[a("el-date-picker",{attrs:{type:"daterange","range-separator":"至","start-placeholder":"开始日期","end-placeholder":"结束日期"},model:{value:t.searchFormData.createTime,callback:function(e){t.$set(t.searchFormData,"createTime",e)},expression:"searchFormData.createTime"}})],1),t._v(" "),a("el-form-item",{attrs:{label:"转移状态",prop:"to_cdn_state_code_id"}},[a("el-select",{staticStyle:{width:"120px"},attrs:{placeholder:"转移状态",clearable:""},model:{value:t.searchFormData.to_cdn_state_code_id,callback:function(e){t.$set(t.searchFormData,"to_cdn_state_code_id",e)},expression:"searchFormData.to_cdn_state_code_id"}},t._l(t.to_cdn_state_list,function(t){return a("el-option",{key:t.codeId,attrs:{label:t.codeValue,value:t.codeId}})}),1)],1),t._v(" "),a("div",{staticClass:"v-search-opt",attrs:{height:t.getTableHeight(50)}},[a("div",{staticClass:"v-inline"},[a("el-button",{attrs:{size:"mini",type:"primary"},on:{click:t.onSearch}},[a("i",{staticClass:"iconfont icon-chaxun"}),t._v(" 查询")]),t._v(" "),a("el-button",{attrs:{size:"mini",type:"primary"},on:{click:t.onReset}},[a("i",{staticClass:"iconfont icon-chongzhi"}),t._v(" 重置")])],1),t._v(" "),a("div",{staticClass:"v-pagination"},[a("el-pagination",{attrs:{"current-page":t.searchFormData.pageNum,"page-size":t.searchFormData.pageSize,total:t.searchFormData.pageCount,"page-sizes":[16,30,50,100],layout:"total, sizes, prev, pager, next, jumper"},on:{"size-change":t.handleSizeChange,"current-change":t.handleCurrentChange}})],1)])],1),t._v(" "),a("div",{staticStyle:{"padding-top":"18px"}},[a("el-table",{attrs:{data:t.tableData,border:!0,stripe:!0,size:"mini",height:t.getTableHeight(100)}},[a("el-table-column",{attrs:{fixed:"",type:"index",index:t.onIndexMethod(t.searchFormData.pageNum,t.searchFormData.pageSize),label:"序号",width:"60"}}),t._v(" "),a("el-table-column",{attrs:{fixed:"left",label:"操作",width:"80"},scopedSlots:t._u([{key:"default",fn:function(e){return[a("el-row",{attrs:{gutter:18}},[a("el-col",{attrs:{span:8}},[a("el-tooltip",{attrs:{effect:"dark",content:"下载",placement:"left"}},[a("el-button",{attrs:{type:"text",size:"mini"},nativeOn:{click:function(a){return a.preventDefault(),t.downloadFile(e.$index,t.tableData)}}},[a("i",{staticClass:"iconfont icon-icon"})])],1)],1),t._v(" "),"2"!==e.row.to_cdn_state_code_id?a("el-col",{attrs:{span:16}},[a("el-tooltip",{attrs:{effect:"dark",content:"重新转移",placement:"left"}},[a("el-button",{attrs:{type:"text",size:"mini"},nativeOn:{click:function(a){return a.preventDefault(),t.retransmission(e.$index,t.tableData)}}},[a("i",{staticClass:"iconfont icon-zhongxinshangchuan"})])],1)],1):a("el-col",{attrs:{span:16}},[a("el-tooltip",{attrs:{effect:"dark",content:"再次转移",placement:"left"}},[a("el-button",{attrs:{type:"text",size:"mini"},nativeOn:{click:function(a){return a.preventDefault(),t.retransmission(e.$index,t.tableData)}}},[a("i",{staticClass:"iconfont icon-zhongxinshangchuan icon-red"})])],1)],1)],1)]}}])}),t._v(" "),a("el-table-column",{attrs:{fixed:"",prop:"filePath",label:"文件信息",width:"220px"},scopedSlots:t._u([{key:"default",fn:function(e){return[a("el-popover",{attrs:{trigger:"hover",placement:"top"}},[a("el-form",{attrs:{"label-width":"120px",size:"mini"}},[a("el-form-item",{attrs:{label:"服务器路径:"}},[a("el-input",{staticStyle:{width:"350px"},model:{value:e.row.filePath,callback:function(a){t.$set(e.row,"filePath",a)},expression:"scope.row.filePath"}})],1),t._v(" "),a("el-form-item",{attrs:{label:"CDN路径:"}},[a("el-input",{model:{value:e.row.fileCdnPath,callback:function(a){t.$set(e.row,"fileCdnPath",a)},expression:"scope.row.fileCdnPath"}})],1),t._v(" "),a("el-form-item",{attrs:{label:"HTTP路径:"}},[a("el-input",{model:{value:"http:/"+e.row.fileCdnPath,callback:function(a){t.$set("http:/"+e.row,"fileCdnPath",a)},expression:"'http:/'+scope.row.fileCdnPath"}})],1)],1),t._v(" "),a("div",{staticClass:"name-wrapper",attrs:{slot:"reference"},slot:"reference"},[a("el-tag",{attrs:{size:"medium"}},[t._v(t._s(e.row.fileName))])],1)],1)]}}])}),t._v(" "),a("el-table-column",{attrs:{fixed:"",prop:"createTime",label:"上传时间",width:"160"}}),t._v(" "),a("el-table-column",{attrs:{prop:"creator",label:"上传者","show-overflow-tooltip":!0,width:"60"}}),t._v(" "),a("el-table-column",{attrs:{prop:"upload_mode_code_id",label:"上传方式","show-overflow-tooltip":!0,width:"80",formatter:t.format_upload_mode_type}}),t._v(" "),a("el-table-column",{attrs:{prop:"upload_project_id",label:"所属项目",width:"120","show-overflow-tooltip":!0,formatter:t.format_upload_project}}),t._v(" "),a("el-table-column",{attrs:{"show-overflow-tooltip":!0,prop:"reliability_state_code_id",label:"可靠性",width:"100",formatter:t.formatIsToCDN},scopedSlots:t._u([{key:"default",fn:function(e){return[a("a",[a("i",{class:"iconfont icon-dian "+t.format_reliability_state_style(e.row,"reliability_state_code_id")}),t._v(t._s(" "+t.format_reliability_state(e.row)))])]}}])}),t._v(" "),a("el-table-column",{attrs:{prop:"isToCdn",label:"已转移",width:"60",formatter:t.formatIsToCDN}}),t._v(" "),a("el-table-column",{attrs:{"show-overflow-tooltip":!0,prop:"fileSize",label:"文件大小",width:"80"}}),t._v(" "),a("el-table-column",{attrs:{"show-overflow-tooltip":!0,prop:"toCdnConsumedTime",label:"转移耗时/s",width:"100"}}),t._v(" "),a("el-table-column",{attrs:{fixed:"right",width:"90",prop:"to_cdn_state_code_id",label:"转移状态",formatter:t.format_to_cdn_state}}),t._v(" "),a("el-table-column",{attrs:{fixed:"right",width:"90",prop:"upload_state_code_id",label:"上传状态",formatter:t.format_upload_state}})],1)],1)],1)},staticRenderFns:[]};var i=a("VU/8")(o,l,!1,function(t){a("2LZq")},"data-v-a9b4970a",null).exports,s={name:"cdnUpload",data(){return{module_name:"cdnUpload",refresh_page_method:"refresh_"+this.module_name,attrs:{accept:"image/*"},statusText:{success:"上传成功",error:"上传出错",uploading:"上传中",paused:"暂停中",waiting:"等待中"},upload_project_info_List:null,to_cdn_rule_code_list:null,pageData:{serviceName:"OAMP_uploadFile",to_cdn_rule_code_id:"",upload_project_id:"",isToCdn:!0,cdnRootPath:"请设置cnd根地址",upload_mode_code_id:""},uploadState:"ready",isCreateUploader:!1}},computed:{options:()=>({target:window.location.origin+"/"+window.location.pathname.split("/")[1]+"/uploadFile",testChunks:!1,chunkSize:4194304,forceChunkSize:!1,fileParameterName:!0,query:{},headers:{},withCredentials:!1,method:"multipart",speedSmoothingFactor:.02})},async mounted(){this.to_cdn_rule_code_list=await this.$setCodeList(this.to_cdn_rule_code_list,"to_cdn_rule"),this.set_upload_project()},methods:{changeToCDNState(){this.pageData.isToCdn||(this.pageData.cdnRootPath=null,this.pageData.upload_project_id=null,this.pageData.to_cdn_rule_code_id=null),this.createUploader()},createUploader(){this.options.query=this.pageData,this.pageData.isToCdn&&null==this.pageData.cdnRootPath?this.isCreateUploader=!1:(this.isCreateUploader=!0,this.uploadState="ready")},async set_upload_project(){if(!this.upload_project_info_List){let t=await this.$search({project_type_code_id:"CDN"},"OAMP_search_project_code_list");null!=t&&(this.upload_project_info_List=t.data)}},async r_get_tool_info(t){let e=new this.$http,{data:a}=await e.post(t,"OAMP_get_tool_info");return null!=a&&"null"!==a&&null!=a.data&&a.data.length>0?a.data[0]:null},async changeProject(t){let e={tool_type_code_id:t},a=await this.r_get_tool_info(e);null==a?this.pageData.cdnRootPath="未获取到cdn根路径信息":(this.pageData.cdnRootPath=a.toolRootPath,this.createUploader())},confirmUpload(){this.pageData.upload_mode_code_id="1",this.upload()},forceUpload(){this.pageData.upload_mode_code_id="2",this.upload()},overUpload(){this.pageData.upload_mode_code_id="3",this.upload()},upload(){let t=this.$refs.uploadRef.uploader;t.getSize()>0?(t.upload(),this.uploadState="upload"):(this.$message.warning("请添加上传文件"),this.uploadState="ready")},pauseUpload(){this.$refs.uploadRef.uploader.pause(),this.uploadState="pause"},resumeUpload(){this.$refs.uploadRef.uploader.resume(),this.uploadState="upload"},cancelUpload(){this.$refs.uploadRef.uploader.cancel()},fileSuccess(t,e,a,o){let l=JSON.parse(o.xhr.response),i="error";console.log(l.code),console.log(typeof l.code),"1"===l.code&&(i="success"),"2"!==l.code&&"3"!==l.code||(i="warning"),console.log(i),this.$notify({type:i,message:l.msg}),this.$refs.uploadRef.uploader.removeFile(e)},fileComplete(t){this.uploadState="ready",this.$emit_method(this.refresh_page_method)}}},r={render:function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",[a("el-form",{staticStyle:{width:"500px"},attrs:{model:t.pageData,size:"mini","label-width":"120px"}},[a("el-form-item",{attrs:{label:"上传CDN"}},[a("el-switch",{attrs:{"active-color":"#13ce66","inactive-color":"#ff4949"},on:{change:t.changeToCDNState},model:{value:t.pageData.isToCdn,callback:function(e){t.$set(t.pageData,"isToCdn",e)},expression:"pageData.isToCdn"}})],1),t._v(" "),t.pageData.isToCdn?a("el-form-item",{attrs:{label:"项目名称"}},[a("el-col",{attrs:{span:20}},[a("el-select",{staticStyle:{width:"100%"},attrs:{placeholder:"项目名称",clearable:""},on:{change:function(e){return t.changeProject(t.pageData.upload_project_id)}},model:{value:t.pageData.upload_project_id,callback:function(e){t.$set(t.pageData,"upload_project_id",e)},expression:"pageData.upload_project_id"}},t._l(t.upload_project_info_List,function(t){return a("el-option",{key:t.project,attrs:{label:t.project_name,value:t._id}})}),1)],1)],1):t._e(),t._v(" "),t.pageData.isToCdn?a("el-form-item",{attrs:{label:"CDN目录规则"}},[a("el-col",{attrs:{span:20}},[a("el-select",{staticStyle:{width:"100%"},attrs:{placeholder:"CDN目录规则",clearable:""},model:{value:t.pageData.to_cdn_rule_code_id,callback:function(e){t.$set(t.pageData,"to_cdn_rule_code_id",e)},expression:"pageData.to_cdn_rule_code_id"}},t._l(t.to_cdn_rule_code_list,function(t){return a("el-option",{key:t.codeId,attrs:{label:t.codeValue,value:t.codeId}})}),1)],1)],1):t._e(),t._v(" "),t.pageData.isToCdn?a("el-form-item",{attrs:{label:"CDN根路径:",prop:"cdnRootPath"}},[t._v(t._s(t.pageData.cdnRootPath))]):t._e(),t._v(" "),t.isCreateUploader?a("el-form-item",[a("el-col",{attrs:{span:24}},["ready"===t.uploadState?a("el-button",{attrs:{type:"primary"},on:{click:t.confirmUpload}},[t._v("通用上传")]):t._e(),t._v(" "),"ready"===t.uploadState?a("el-button",{attrs:{type:"primary"},on:{click:t.forceUpload}},[t._v("强制上传")]):t._e(),t._v(" "),"ready"===t.uploadState?a("el-button",{attrs:{type:"primary"},on:{click:t.overUpload}},[t._v("覆盖上传")]):"upload"===t.uploadState?a("el-button",{attrs:{type:"primary"},on:{click:t.pauseUpload}},[t._v("暂停上传")]):a("el-button",{attrs:{type:"primary"},on:{click:t.resumeUpload}},[t._v("继续上传")]),t._v(" "),a("el-button",{attrs:{type:"primary"},on:{click:t.cancelUpload}},[t._v("取消上传")])],1)],1):t._e()],1),t._v(" "),t.isCreateUploader?a("uploader",{ref:"uploadRef",staticClass:"uploader-example",attrs:{options:t.options,"file-status-text":t.statusText,autoStart:!1},on:{"file-success":t.fileSuccess,"file-complete":t.fileComplete}},[a("uploader-unsupport"),t._v(" "),a("uploader-drop",{staticStyle:{"text-align":"center"}},[a("p",[t._v("拖拽文件至此上传")]),t._v(" "),a("uploader-btn",[t._v("选择文件")]),t._v(" "),a("uploader-btn",{attrs:{attrs:t.attrs}},[t._v("选择图片")]),t._v(" "),a("uploader-btn",{attrs:{directory:!0}},[t._v("选择文件夹")])],1),t._v(" "),t.pageData.isToCdn?a("uploader-list",{ref:"uploadListRef",staticStyle:{"max-height":"500px","overflow-y":"scroll","overflow-x":"hidden"},attrs:{id:"style-7"}}):a("uploader-list",{ref:"uploadListRef",staticStyle:{"max-height":"641px","overflow-y":"scroll","overflow-x":"hidden"},attrs:{id:"style-7"}})],1):t._e()],1)},staticRenderFns:[]};var n={name:"cdn",components:{cdnUploadRecordList:i,cndUpload:a("VU/8")(s,r,!1,function(t){a("YN9p")},null,null).exports},data:()=>({activeName:"cndUpload"}),methods:{handleClick(t,e){}}},d={render:function(){var t=this.$createElement,e=this._self._c||t;return e("el-row",{attrs:{gutter:5}},[e("el-col",{attrs:{span:8}},[e("cndUpload")],1),this._v(" "),e("el-col",{attrs:{span:16}},[e("cdnUploadRecordList")],1)],1)},staticRenderFns:[]};var c=a("VU/8")(n,d,!1,function(t){a("6tni")},null,null);e.default=c.exports},YN9p:function(t,e){}});
//# sourceMappingURL=4.4acd61cfd69d6ae02cf7.js.map