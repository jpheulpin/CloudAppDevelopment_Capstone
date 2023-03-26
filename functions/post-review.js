function main(params) {
    return new Promise(function (resolve, reject) {
      const { CloudantV1 } = require("@ibm-cloud/cloudant");
      const { IamAuthenticator } = require("ibm-cloud-sdk-core");
      const authenticator = new IamAuthenticator({
        apikey: "",
      });
      const cloudant = CloudantV1.newInstance({
        authenticator: authenticator,
      });
      cloudant.setServiceUrl("");
      cloudant
        .postDocument({
          db: "reviews",
          document: params.review,
        })
        .then((result) => {
          let code = 201;
          resolve({
            statusCode: code,
            headers: { "Content-Type": "application/json" },
          });
        })
        .catch((err) => {
          reject(err);
        });
    });
  }