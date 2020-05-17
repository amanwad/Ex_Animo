import { Meteor } from 'meteor/meteor';
import { Patients } from '../imports/api/patients.js';

const { Storage } = require('@google-cloud/storage');
//{keyFilename: "key.json"}
//export const Patients = new Mongo.Collection('patients');

// signed URL not working with parameters
const storage = new Storage({
  keyFilename: "/Users/amanwadhwa/WebApps/physV1/server/key.json",
  projectId: "hackathon-276705"});

Meteor.startup(() => {
  // code to run on server at startup
  }
);

Meteor.methods({
      async getDates(currPatient){
        var [buckets] = await storage.getBuckets();
        var dates = []
        buckets.forEach(bucket => {
          var arrStr = bucket.name.split("_");
          var name = arrStr[0];
          var doctor = arrStr[1];
          var date = arrStr[2];
          
          var hyphen = name.indexOf("-");
          var firstName = name.substring(0,1).toUpperCase().concat(name.substring(1,hyphen));
          var lastName = name.substring(hyphen+1, hyphen+2).toUpperCase().concat(name.substring(hyphen+2));
          var patientName = firstName.concat(" ").concat(lastName);
          if(doctor==this.userId.toLowerCase() && patientName==currPatient){
            dates.push(date);
          }
        });
        return dates;
      },
    addPatients(name,gender,dob,blood,pre){
      Patients.insert({name:name,doctor:this.userId,gender:gender,dob:dob,blood:blood,pre:pre}); //add all info for patient
    },
    async generateSignedUrl( bucketName, fileName ) {
      const options = {
        version: 'v4',
        action: 'read',
        expires: Date.now() + 60 * 60 * 1000
      };
      const [url] = await storage.bucket(bucketName).file(fileName).getSignedUrl(options);
      return url;
    },
    removeAllPatients(){
      Patients.remove({});
    },
    async listFiles(bucketName) {
      // Lists files in the bucket
      const [files] = await storage.bucket(bucketName).getFiles();
      // var names = []
      // files.forEach(file => {
      //   names.push(file.name)
      // });
      return files;
    },
    async testing(currPatient){
      var [buckets] = await storage.getBuckets();
      var dates = []
      buckets.forEach(bucket => {
        var arrStr = bucket.name.split("_");
        var name = arrStr[0];
        var doctor = arrStr[1];
        var date = arrStr[2];
        
        var hyphen = name.indexOf("-");
        var firstName = name.substring(0,1).toUpperCase().concat(name.substring(1,hyphen));
        var lastName = name.substring(hyphen+1, hyphen+2).toUpperCase().concat(name.substring(hyphen+2));
        var patientName = firstName.concat(" ").concat(lastName);
        if(doctor==this.userId.toLowerCase() && patientName==currPatient){
          dates.push(date);
        }
      });
      return dates;
    }
  });