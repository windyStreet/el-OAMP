webpackJsonp([5],{EjWi:function(e,t,a){"use strict";Object.defineProperty(t,"__esModule",{value:!0});var n={name:"sysUpdateManageList",data(){return{module_name:"sysUpdateManage",refresh_page_method:"refresh_"+this.module_name,searchFormData:{pageNum:1,pageSize:14,pageCount:1,order:"+createTime"},tableData:[]}},created(){this.$store.state.Apps.$on(this.refresh_page_method,()=>{this.search()})},async mounted(){this.search()},methods:{handleSizeChange(e){this.searchFormData.pageSize=e,this.search()},handleCurrentChange(e){this.searchFormData.pageNum=e,this.search()},onReset(){this.$refs.searchFormRef.resetFields(),this.search()},onSearch(){this.searchFormData.pageNum=1,this.search()},async search(){let e=await this.$search(this.searchFormData,"OAMP_search_sys_update_info_list");this.searchFormData.pageCount=e.pageCount,this.tableData=e.data;for(var t=0;t<this.tableData.length;t++){let e="";for(var a=0;a<this.tableData[String(t)].version_content.length;a++)e+=String(a+1)+". "+this.tableData[String(t)].version_content[a]+"   ";this.tableData[String(t)].version_content_format=e.replace(/(\s*$)/g,"")}},async onDelete(e,t){let a=t[e];this.$del(a,"OAMP_delete_sys_update_info")?(t.splice(e,1),this.$message.success("删除数据成功"),this.search()):this.$message.error("删除数据失败")}}},s={render:function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("div",{staticStyle:{"padding-top":"2px"}},[a("el-form",{ref:"searchFormRef",attrs:{inline:!0,model:e.searchFormData,size:"mini"}},[a("el-form-item",{attrs:{label:"更新版本号",prop:"version_number"}},[a("el-input",{attrs:{placeholder:"请输入更新版本号"},model:{value:e.searchFormData.version_number,callback:function(t){e.$set(e.searchFormData,"version_number",t)},expression:"searchFormData.version_number"}})],1),e._v(" "),a("el-form-item",{attrs:{label:"更新内容",prop:"version_content"}},[a("el-input",{attrs:{placeholder:"请输入更新内容"},model:{value:e.searchFormData.version_content,callback:function(t){e.$set(e.searchFormData,"version_content",t)},expression:"searchFormData.version_content"}})],1),e._v(" "),a("el-form-item",{attrs:{label:"更新时间",prop:"version_update_time"}},[a("el-date-picker",{attrs:{type:"datetimerange","start-placeholder":"开始日期","end-placeholder":"结束日期","value-format":"yyyy-MM-dd HH:mm","default-time":["00:00:00","23:59:59"]},model:{value:e.searchFormData.version_update_time,callback:function(t){e.$set(e.searchFormData,"version_update_time",t)},expression:"searchFormData.version_update_time"}})],1),e._v(" "),a("div",{staticClass:"v-search-opt"},[a("div",{staticClass:"v-pagination"},[a("el-pagination",{attrs:{"current-page":e.searchFormData.pageNum,"page-size":e.searchFormData.pageSize,total:e.searchFormData.pageCount,"page-sizes":[14,20,50,100],layout:"total, sizes, prev, pager, next, jumper"},on:{"size-change":e.handleSizeChange,"current-change":e.handleCurrentChange}})],1),e._v(" "),a("div",{staticClass:"v-inline"},[a("el-button",{attrs:{size:"mini",type:"primary"},on:{click:e.onSearch}},[a("i",{staticClass:"iconfont icon-chaxun"}),e._v(" 查询")]),e._v(" "),a("el-button",{attrs:{size:"mini",type:"primary"},on:{click:e.onReset}},[a("i",{staticClass:"iconfont icon-chongzhi"}),e._v(" 重置")]),e._v(" "),a("el-button",{attrs:{size:"mini",type:"primary"},on:{click:function(t){return e.onAdd(e.module_name)}}},[a("i",{staticClass:"iconfont icon-xinzeng"}),e._v(" 新增")])],1)])],1),e._v(" "),a("hr"),e._v(" "),a("el-table",{attrs:{data:e.tableData,border:!0,stripe:!0,size:"mini",height:e.getTableHeight(130)}},[a("el-table-column",{attrs:{fixed:"",type:"index",index:e.onIndexMethod(e.searchFormData.pageNum,e.searchFormData.pageSize),label:"序号",width:"50"}}),e._v(" "),a("el-table-column",{attrs:{prop:"version_number",label:"更新版本号",width:"85"}}),e._v(" "),a("el-table-column",{attrs:{prop:"version_update_time",label:"更新时间",width:"135"}}),e._v(" "),a("el-table-column",{attrs:{prop:"creator",label:"创建人",width:"70"}}),e._v(" "),a("el-table-column",{attrs:{prop:"createTime",label:"创建时间",width:"156"}}),e._v(" "),a("el-table-column",{attrs:{"show-overflow-tooltip":!0,property:"version_content_format",label:"更新内容"}}),e._v(" "),a("el-table-column",{attrs:{"show-overflow-tooltip":!0,property:"remark",width:"180",label:"备注"}}),e._v(" "),a("el-table-column",{attrs:{fixed:"right",label:"操作",width:"160"},scopedSlots:e._u([{key:"default",fn:function(t){return[a("el-col",{attrs:{span:8}},[a("el-tooltip",{staticClass:"item",attrs:{effect:"dark",content:"查看",placement:"left"}},[a("el-button",{attrs:{type:"text",size:"small"},nativeOn:{click:function(a){return a.preventDefault(),e.onView(e.module_name,t.$index,e.tableData)}}},[a("i",{staticClass:"iconfont icon-chakan"})])],1)],1),e._v(" "),a("el-col",{attrs:{span:8}},[a("el-tooltip",{staticClass:"item",attrs:{effect:"dark",content:"修改",placement:"left"}},[a("el-button",{attrs:{type:"text",size:"small"},nativeOn:{click:function(a){return a.preventDefault(),e.onEdit(e.module_name,t.$index,e.tableData)}}},[a("i",{staticClass:"iconfont icon-xiugai"})])],1)],1),e._v(" "),a("el-col",{attrs:{span:8}},[a("el-tooltip",{staticClass:"item",attrs:{effect:"dark",content:"删除",placement:"left"}},[a("el-button",{attrs:{type:"text",size:"small"},nativeOn:{click:function(a){return a.preventDefault(),e.onDelete(t.$index,e.tableData)}}},[a("i",{staticClass:"iconfont icon-shanchu icon-red"})])],1)],1)]}}])})],1)],1)},staticRenderFns:[]};var o=a("VU/8")(n,s,!1,function(e){a("u+bo")},"data-v-49984332",null).exports,r={name:"sysUpdateManageInfo",data(){return{module_name:"sysUpdateManage",refresh_page_method:"refresh_"+this.module_name,pageData:{version_content:[""]},pageDataRules:{version_number:[{required:!0,message:"请输入更新版本号",trigger:"blur"}],version_update_time:[{required:!0,message:"请输入选择日期",trigger:"blur"}]}}},computed:{pageInfo(){let e=this.$setPageInfo(this.module_name);return"add"===e.pageModel?this.pageData={version_content:[""]}:"edit"!==e.pageModel||null!==e.pageData&&0!==e.pageData.version_content.length||(this.pageData={version_content:[""]},this.pageData=e.pageData),e}},methods:{addContent(){this.pageData.version_content.push("")},removeContent(){this.pageData.version_content.length>=2&&this.pageData.version_content.pop()},onSubmit(){let e=this;this.$refs.pageDataRef.validate(async t=>{if(t){let t=e.pageData,a=[];if(this.pageData.version_content.forEach(e=>{e&&a.push(e)}),0==a.length)return void alert("更新内容不能为空");t.version_content=a,null!==await e.$insert(t,"OAMP_insert_sys_update_info")?(e.$message.success("新增信息成功"),e.$onClose(e.module_name,"pageDataRef",e.refresh_page_method)):e.$message.error("新增信息失败")}})},async onUpdate(){let e=this;this.$refs.pageDataRef.validate(async t=>{if(t){let t=e.pageData,a=[];if(this.pageData.version_content.forEach(e=>{e&&a.push(e)}),0==a.length)return void alert("更新内容不能为空");t.version_content=a,null!=await e.$update(t,"OAMP_update_sys_update_info")?(e.$message.success("修改信息成功"),e.$onClose(e.module_name,"pageDataRef",e.refresh_page_method)):e.$message.error("修改信息失败")}})}}},i={render:function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("el-dialog",{attrs:{title:"系统更新信息",visible:e.pageInfo.isShow,"modal-append-to-body":!1,"close-on-click-modal":!1,center:!0,"lock-scroll":!1},on:{close:function(t){return e.onClose(e.module_name,"pageDataRef")}}},[a("el-form",{ref:"pageDataRef",attrs:{model:e.pageData,rules:e.pageDataRules,inline:!0,"label-width":"160px",size:"small"}},[a("el-form-item",{attrs:{label:"更新版本",prop:"version_number"}},[a("el-input",{model:{value:e.pageData.version_number,callback:function(t){e.$set(e.pageData,"version_number",t)},expression:"pageData.version_number"}})],1),e._v(" "),a("el-form-item",{attrs:{label:"更新时间",prop:"version_update_time"}},[a("el-date-picker",{attrs:{type:"datetime",placeholder:"选择日期时间","value-format":"yyyy-MM-dd HH:mm:ss"},model:{value:e.pageData.version_update_time,callback:function(t){e.$set(e.pageData,"version_update_time",t)},expression:"pageData.version_update_time"}})],1),e._v(" "),a("el-form-item",{attrs:{label:"更新内容",prop:"version_content"}},[e._l(e.pageData.version_content,function(t,n){return"add"===e.pageInfo.pageModel?a("el-row",{key:n},[a("el-col",{staticClass:"contentIndex",attrs:{span:1}},[e._v(e._s(n+1)+".")]),e._v(" "),a("el-col",{attrs:{span:14}},[a("el-input",{staticStyle:{width:"696px"},attrs:{type:"textarea",autosize:{minRows:1,maxRows:5}},model:{value:e.pageData.version_content[n],callback:function(t){e.$set(e.pageData.version_content,n,t)},expression:"pageData.version_content[index]"}})],1)],1):e._e()}),e._v(" "),e._l(e.pageData.version_content,function(t,n){return"edit"===e.pageInfo.pageModel||"view"===e.pageInfo.pageModel?a("el-row",{key:n},[a("el-col",{staticClass:"contentIndex",staticStyle:{},attrs:{span:1}},[e._v(e._s(n+1)+".")]),e._v(" "),a("el-col",{attrs:{span:14}},[a("el-input",{staticStyle:{width:"696px"},attrs:{type:"textarea",autosize:{minRows:1,maxRows:5}},model:{value:e.pageData.version_content[n],callback:function(t){e.$set(e.pageData.version_content,n,t)},expression:"pageData.version_content[index]"}})],1)],1):e._e()}),e._v(" "),"add"===e.pageInfo.pageModel||"edit"===e.pageInfo.pageModel?a("el-row",{attrs:{gutter:10}},[a("el-col",{attrs:{span:3,offset:7}},[a("el-tooltip",{attrs:{content:"添加更新内容条目",placement:"top"}},[a("el-button",{attrs:{type:"primary"},on:{click:e.addContent}},[a("i",{staticClass:"el-icon-circle-plus-outline"}),e._v(" 新增")])],1)],1),e._v(" "),a("el-col",{attrs:{span:3,offset:1}},[a("el-tooltip",{attrs:{content:"删除更新内容条目",placement:"top"}},[a("el-button",{attrs:{type:"primary"},on:{click:e.removeContent}},[a("i",{staticClass:"el-icon-remove-outline"}),e._v(" 移除")])],1)],1)],1):e._e()],2),e._v(" "),a("el-form-item",{attrs:{label:"备注",prop:"remark"}},[a("el-input",{staticStyle:{width:"696px"},attrs:{type:"textarea"},model:{value:e.pageData.remark,callback:function(t){e.$set(e.pageData,"remark",t)},expression:"pageData.remark"}})],1)],1),e._v(" "),a("div",{staticClass:"dialog-footer",attrs:{slot:"footer"},slot:"footer"},[a("el-button",{on:{click:function(t){return e.onClose(e.module_name,"pageDataRef")}}},[e._v("关 闭")]),e._v(" "),"add"===e.pageInfo.pageModel?a("el-button",{attrs:{type:"primary"},on:{click:e.onSubmit}},[e._v("确 定")]):"edit"===e.pageInfo.pageModel?a("el-button",{attrs:{type:"primary"},on:{click:e.onUpdate}},[e._v("更 新")]):e._e()],1)],1)},staticRenderFns:[]};var l={name:"sysUpdateManage",components:{list:o,info:a("VU/8")(r,i,!1,function(e){a("Iuk1")},"data-v-9f96d5b8",null).exports}},c={render:function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("div",{staticClass:"v-container"},[a("el-breadcrumb",[a("el-breadcrumb-item",{attrs:{to:{name:"setting"}}},[e._v("设置")]),e._v(" "),a("el-breadcrumb-item",{attrs:{to:{name:"sysManage"}}},[e._v("系统管理")]),e._v(" "),a("el-breadcrumb-item",[e._v("系统更新信息管理")])],1),e._v(" "),a("hr"),e._v(" "),a("list"),e._v(" "),a("info")],1)},staticRenderFns:[]};var p=a("VU/8")(l,c,!1,function(e){a("Yk3R")},"data-v-4ffd35c7",null);t.default=p.exports},Iuk1:function(e,t){},Yk3R:function(e,t){},"u+bo":function(e,t){}});
//# sourceMappingURL=5.7f790ab5e2ce814faf78.js.map