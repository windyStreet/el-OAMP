webpackJsonp([16],{"3ijl":function(e,t,a){"use strict";Object.defineProperty(t,"__esModule",{value:!0});var o={name:"codeManageList",data(){return{module_name:"codeManage",refresh_page_method:"refresh_"+this.module_name,searchFormData:{pageNum:1,pageSize:14,pageCount:1,onlyShowCodeType:!0,code:"",codeName:"",order:"+code"},tableData:[]}},created(){this.$store.state.Apps.$on(this.refresh_page_method,()=>{this.search()})},async mounted(){this.search()},methods:{handleSizeChange(e){this.searchFormData.pageSize=e,this.search()},handleCurrentChange(e){this.searchFormData.pageNum=e,this.search()},onReset(){this.$refs.searchFormRef.resetFields(),this.search()},formatCodeTypeBoolean:(e,t,a)=>!0===e.isCodeType?"代码类型":"代码值",setShowType(){this.search()},async r_search_list(e){let t=new this.$http,{data:a}=await t.post(e,"OAMP_search_code_info_list");this.searchFormData.pageCount=a.pageCount,this.tableData=a.data},async r_delete_code_type_info(e){let t=new this.$http,{data:a}=await t.post(e,"OAMP_delete_code_type_info");return null!=a&&"null"!==a},onSearch(){this.searchFormData.pageNum=1,this.search()},search(){let e=this.searchFormData;this.r_search_list(e)},onDelete(e,t){let a=t[e];this.r_delete_code_type_info(a)?(t.splice(e,1),this.$message.success("删除数据成功"),this.search()):this.$message.error("删除数据失败")},on_project_configure(e,t){}}},s={render:function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("div",{staticStyle:{"padding-top":"2px"}},[a("el-form",{ref:"searchFormRef",attrs:{inline:!0,model:e.searchFormData,size:"mini"}},[a("el-form-item",{attrs:{label:"代码表名称"}},[a("el-input",{attrs:{placeholder:"代码表名称"},model:{value:e.searchFormData.code,callback:function(t){e.$set(e.searchFormData,"code",t)},expression:"searchFormData.code"}})],1),e._v(" "),a("el-form-item",{attrs:{label:"代码表中文名称"}},[a("el-input",{attrs:{placeholder:"代码表中文名称"},model:{value:e.searchFormData.codeName,callback:function(t){e.$set(e.searchFormData,"codeName",t)},expression:"searchFormData.codeName"}})],1),e._v(" "),a("el-form-item",[a("el-switch",{attrs:{"active-text":"仅显示代码类型","inactive-text":"全部显示",size:"mini"},on:{change:function(t){return e.setShowType(e.searchFormData.onlyShowCodeType)}},model:{value:e.searchFormData.onlyShowCodeType,callback:function(t){e.$set(e.searchFormData,"onlyShowCodeType",t)},expression:"searchFormData.onlyShowCodeType"}})],1),e._v(" "),a("div",{staticClass:"v-search-opt"},[a("div",{staticClass:"v-pagination"},[a("el-pagination",{attrs:{"current-page":e.searchFormData.pageNum,"page-size":e.searchFormData.pageSize,total:e.searchFormData.pageCount,"page-sizes":[14,20,50,100],layout:"total, sizes, prev, pager, next, jumper"},on:{"size-change":e.handleSizeChange,"current-change":e.handleCurrentChange}})],1),e._v(" "),a("div",{staticClass:"v-inline"},[a("el-button",{attrs:{size:"mini",type:"primary"},on:{click:e.onSearch}},[a("i",{staticClass:"iconfont icon-chaxun"}),e._v(" 查询")]),e._v(" "),a("el-button",{attrs:{size:"mini",type:"primary"},on:{click:e.onReset}},[a("i",{staticClass:"iconfont icon-chongzhi"}),e._v(" 重置")]),e._v(" "),a("el-button",{attrs:{size:"mini",type:"primary"},on:{click:function(t){return e.onAdd(e.module_name)}}},[a("i",{staticClass:"iconfont icon-xinzeng"}),e._v(" 新增")])],1)])],1),e._v(" "),a("hr"),e._v(" "),a("el-table",{attrs:{data:e.tableData,border:!0,stripe:!0,size:"mini",height:e.getTableHeight(130)}},[a("el-table-column",{attrs:{fixed:"",type:"index",index:e.onIndexMethod(e.searchFormData.pageNum,e.searchFormData.pageSize),label:"序号",width:"60"}}),e._v(" "),a("el-table-column",{attrs:{fixed:"",prop:"isCodeType",label:"类别",width:"120",formatter:e.formatCodeTypeBoolean}}),e._v(" "),a("el-table-column",{attrs:{fixed:"",prop:"code",label:"代码表名称",width:"180"}}),e._v(" "),a("el-table-column",{attrs:{prop:"codeName",label:"代码表中文名称",width:"180"}}),e._v(" "),a("el-table-column",{attrs:{prop:"codeId",label:"代码ID",width:"180"}}),e._v(" "),a("el-table-column",{attrs:{prop:"codeValue",label:"代码值",width:"180"}}),e._v(" "),a("el-table-column",{attrs:{prop:"fatherCode",label:"父级代码",width:"180"}}),e._v(" "),a("el-table-column",{attrs:{prop:"createTime",label:"创建时间"}}),e._v(" "),a("el-table-column",{attrs:{prop:"updateTime",label:"修改时间"}}),e._v(" "),a("el-table-column",{attrs:{prop:"remark",label:"备注"}}),e._v(" "),a("el-table-column",{attrs:{fixed:"right",label:"操作",width:"120"},scopedSlots:e._u([{key:"default",fn:function(t){return[a("el-row",{attrs:{gutter:10}},[a("el-col",{attrs:{span:8}},[t.row.isCodeType?a("el-tooltip",{staticClass:"item",attrs:{effect:"dark",content:"修改",placement:"left"}},[a("el-button",{attrs:{type:"text",size:"small"},nativeOn:{click:function(a){return a.preventDefault(),e.onEdit(e.module_name,t.$index,e.tableData)}}},[a("i",{staticClass:"iconfont icon-xiugai"})])],1):a("el-col",{staticStyle:{visibility:"hidden"},attrs:{span:8}},[a("el-button")],1)],1),e._v(" "),a("el-col",{attrs:{span:8}},[a("el-tooltip",{staticClass:"item",attrs:{effect:"dark",content:"删除当前代码表",placement:"left"}},[a("el-button",{attrs:{type:"text",size:"small"},nativeOn:{click:function(a){return a.preventDefault(),e.onDelete(t.$index,e.tableData)}}},[a("i",{staticClass:"iconfont icon-shanchu icon-red"})])],1)],1)],1)]}}])})],1)],1)},staticRenderFns:[]};var l=a("VU/8")(o,s,!1,function(e){a("v260")},"data-v-30a3e33a",null).exports,i={name:"codeManageInfo",data(){return{module_name:"codeManage",refresh_page_method:"refresh_"+this.module_name,isDisabled:!1,pageData:{code:"",codeName:"",remark:""},codeData:{codeId:"",codeValue:"",fatherCode:""},codeInfoDataList:[],pageDataRules:{code:[{required:!0,message:"请输入代码名称",trigger:"blur"}],codeName:[{required:!0,message:"请输入代码中文名称",trigger:"blur"}]},codeDataRules:{codeId:[{required:!0,validator:(e,t,a)=>t?(setTimeout(()=>{if(this.codeInfoDataList)for(let e of this.codeInfoDataList)if(e.codeId===t){a(new Error("当前代码已经存在"));break}a()},200),!0):a(new Error("请输入代码")),trigger:"blur"}],codeValue:[{required:!0,message:"请输入code值",trigger:"blur"}]}}},computed:{pageInfo(){this.codeInfoDataList=[],this.isDisabled=!1;let e=this.$setPageInfo(this.module_name);return this.setPageInit(e),e}},methods:{setPageInit(e){if("add"!==e.pageModel&&"default"!==e.pageModel){let t={code:e.pageData.code};this.r_search_code_data_list(t)}},async r_search_code_data_list(e){let t=new this.$http,{data:a}=await t.post(e,"OAMP_search_code_data_list");this.codeInfoDataList=a.data},async r_insert_code_type_info(e){let t=new this.$http,{data:a}=await t.post(e,"OAMP_insert_code_type_info");if(null!=a&&"null"!==a)return a.data},async r_insert_code_data(e){let t=new this.$http,{data:a}=await t.post(e,"OAMP_insert_code_data");if(null!=a&&"null"!==a)return a.data},async r_update_code_type_info(e){let t=new this.$http,{data:a}=await t.post(e,"OAMP_update_code_type_info");if(null!=a&&"null"!==a)return a},async r_delete_code_data(e){let t=new this.$http,{data:a}=await t.post(e,"OAMP_delete_code_data");return null!==a&&"null"!==a},addCodeTypeInfo(){let e=this;this.$refs.pageDataRef.validate(async t=>{if(t){let t=e.pageData,a=await e.r_insert_code_type_info(t);null!=a?(e.codeTypeData=a,e.isDisabled=!0,e.$message.success("新增代码表类型信息成功")):e.$message.error("新增代码表类型信息失败")}})},updateCodeTypeInfo(){let e=this;this.$refs.pageDataRef.validate(async t=>{if(t){let t=e.pageData,a=await e.r_update_code_type_info(t);null!=a?(e.codeTypeData=a,e.isDisabled=!0,e.$message.success("更新代码表类型信息成功")):e.$message.error("更新代码表类型信息失败")}})},addCodeInfoData(){let e=this;this.$refs.codeDataRef.validate(async t=>{if(t){let t={code:e.pageData.code,codeName:e.pageData.codeName,codeId:e.codeData.codeId,codeValue:e.codeData.codeValue,fatherCode:e.codeData.fatherCode,isCodeType:0},a=await e.r_insert_code_data(t);null!=a?(e.$message.success("新增代码表值信息成功"),this.$refs.codeDataRef.resetFields(),e.codeInfoDataList.unshift(a)):e.$message.error("更新代码表类型信息失败")}})},deleteCodeInfoData(e,t){let a=t[e];null!=this.r_delete_code_data(a)?(t.splice(e,1),this.$message.success("删除代码表值信息成功")):this.$message.success("删除代码表值信息失败")},reset(){this.$refs.pageDataRef.resetFields(),this.$refs.codeDataRef.resetFields()}}},r={render:function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("el-dialog",{attrs:{title:"代码表信息",visible:e.pageInfo.isShow,"modal-append-to-body":!1,"close-on-click-modal":!1,center:!0,"lock-scroll":!1},on:{close:function(t){return e.onClose(e.module_name,["pageDataRef","codeDataRef"])}}},[a("el-form",{ref:"pageDataRef",attrs:{model:e.pageData,rules:e.pageDataRules,inline:!0,"label-width":"160px",size:"mini"}},[a("el-form-item",{attrs:{label:"代码表名称",prop:"code"}},[a("el-input",{attrs:{disabled:e.isDisabled},model:{value:e.pageData.code,callback:function(t){e.$set(e.pageData,"code",t)},expression:"pageData.code"}})],1),e._v(" "),a("el-form-item",{attrs:{label:"代码表中文名称",prop:"codeName"}},[a("el-input",{attrs:{disabled:e.isDisabled},model:{value:e.pageData.codeName,callback:function(t){e.$set(e.pageData,"codeName",t)},expression:"pageData.codeName"}})],1),e._v(" "),a("el-form-item",{attrs:{label:"备注",prop:"remark"}},[a("el-input",{staticStyle:{width:"696px"},attrs:{type:"textarea",disabled:e.isDisabled},model:{value:e.pageData.remark,callback:function(t){e.$set(e.pageData,"remark",t)},expression:"pageData.remark"}})],1),e._v(" "),a("div",{staticClass:"v-center"},[a("el-button",{attrs:{type:"primary",size:"mini",disabled:e.isDisabled},on:{click:e.reset}},[e._v("重 置")]),e._v(" "),"add"==e.pageInfo.pageModel?a("el-button",{attrs:{size:"mini",type:"primary",disabled:e.isDisabled},on:{click:e.addCodeTypeInfo}},[e._v("新增代码表类型")]):a("el-button",{attrs:{type:"primary",size:"small",disabled:e.isDisabled},on:{click:e.updateCodeTypeInfo}},[e._v("更新代码表类型")])],1)],1),e._v(" "),a("hr"),e._v(" "),a("el-form",{ref:"codeDataRef",attrs:{model:e.codeData,rules:e.codeDataRules,inline:!0,"label-width":"160px",size:"mini"}},[a("el-form-item",{attrs:{label:"代码","label-width":"160px",prop:"codeId"}},[a("el-input",{staticStyle:{width:"150px"},model:{value:e.codeData.codeId,callback:function(t){e.$set(e.codeData,"codeId",t)},expression:"codeData.codeId"}})],1),e._v(" "),a("el-form-item",{attrs:{label:"代码值","label-width":"80px",prop:"codeValue"}},[a("el-input",{staticStyle:{width:"150px"},model:{value:e.codeData.codeValue,callback:function(t){e.$set(e.codeData,"codeValue",t)},expression:"codeData.codeValue"}})],1),e._v(" "),a("el-form-item",{attrs:{label:"父级代码","label-width":"80px",prop:"fatherCode"}},[a("el-input",{staticStyle:{width:"150px"},model:{value:e.codeData.fatherCode,callback:function(t){e.$set(e.codeData,"fatherCode",t)},expression:"codeData.fatherCode"}})],1),e._v(" "),a("el-form-item",[a("el-button",{attrs:{type:"primary"},on:{click:e.addCodeInfoData}},[e._v("新增")])],1)],1),e._v(" "),a("el-table",{staticStyle:{width:"100%"},attrs:{data:e.codeInfoDataList,prop:"codeInfoDataList","max-height":"250",size:"mini"}},[a("el-table-column",{attrs:{fixed:"",label:"操作",width:"120"},scopedSlots:e._u([{key:"default",fn:function(t){return[a("el-button",{attrs:{type:"text",size:"small"},nativeOn:{click:function(a){return a.preventDefault(),e.deleteCodeInfoData(t.$index,e.codeInfoDataList)}}},[e._v("移除")])]}}])}),e._v(" "),a("el-table-column",{attrs:{type:"index",label:"序号",width:"50"}}),e._v(" "),a("el-table-column",{attrs:{prop:"codeId",label:"代码"}}),e._v(" "),a("el-table-column",{attrs:{prop:"codeValue",label:"代码值"}}),e._v(" "),a("el-table-column",{attrs:{prop:"fatherCode",label:"父级代码"}})],1),e._v(" "),a("div",{staticClass:"dialog-footer",attrs:{slot:"footer"},slot:"footer"},[a("el-button",{attrs:{size:"small"},on:{click:function(t){return e.onClose(e.module_name,["pageDataRef","codeDataRef"])}}},[e._v("关 闭")])],1)],1)},staticRenderFns:[]};var n={name:"codeManage",components:{list:l,info:a("VU/8")(i,r,!1,function(e){a("N/2t")},"data-v-1fdcd5bc",null).exports}},d={render:function(){var e=this.$createElement,t=this._self._c||e;return t("div",{staticClass:"v-container"},[t("el-breadcrumb",[t("el-breadcrumb-item",{attrs:{to:{name:"setting"}}},[this._v("设置")]),this._v(" "),t("el-breadcrumb-item",[this._v("代码表设置")])],1),this._v(" "),t("hr"),this._v(" "),t("list"),this._v(" "),t("info")],1)},staticRenderFns:[]};var c=a("VU/8")(n,d,!1,function(e){a("v9VZ")},"data-v-0d17c8d6",null);t.default=c.exports},"N/2t":function(e,t){},v260:function(e,t){},v9VZ:function(e,t){}});
//# sourceMappingURL=16.d5e744e4b5d0bf5723f5.js.map