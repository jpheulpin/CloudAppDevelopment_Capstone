/**
 * Get all dealerships
 */

const { CloudantV1 } = require('@ibm-cloud/cloudant');
const { IamAuthenticator } = require('ibm-cloud-sdk-core');

const api_key = "AZJlnpzAT43oUx59RvBYwGMlrsSmcHPmWqUdrOUfFgtF";
const url = "https://apikey-v2-32m2roj269pgclzt2sbzsgqgsrjy7es6s422att1y07p:7d410dc7893a4dd5d27fe4147baf1111@a6907094-f3bc-48ce-ab65-9f579fae08f2-bluemix.cloudantnosqldb.appdomain.cloud"

async function main(params) {
      const authenticator = new IamAuthenticator({ apikey: api_key })
      const cloudant = CloudantV1.newInstance({
          authenticator: authenticator
      });
      cloudant.setServiceUrl(url);
      
     return new Promise((resolve, reject) => {
         cloudant.postFind({db:"dealerships", selector:{"state": params.state}})
                 .then((result)=>{
                   resolve({result:result.result.docs});
                 })
                 .catch(err => {
                    console.log(err);
                     reject({ err: err });
                 });
          })
}