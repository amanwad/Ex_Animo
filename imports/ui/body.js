import { Template } from 'meteor/templating';
import { ReactiveVar } from 'meteor/reactive-var';
import { Session } from 'meteor/session';
import { Patients } from '../api/patients.js';
import './body.html';


Session.set("SelectedPatient", "Welcome");
Session.set("FormVar", "Dashboard");
Session.set("SelectedDate", "");
Session.set("Dates", []);
Session.set("Files", []);
Session.set("Dropped", false)
Session.set("URL", "");

Template.body.helpers({
  retSess() {
    return Session.get("SelectedPatient");
  },
  retIfLoggedIn(){
    console.log(Meteor.userId());
    if(Meteor.userId() === null){ //This means that user has NOT logged in
      return false;
    }
    else{
      return true;
    }
  },
  retForm() {
    if(Session.get("FormVar")=="Dashboard") {
      return true;
    }
    return false;
  },
  retId() {
    return Meteor.userId();
  },
  retIfWelcome(){
    if(Session.get("SelectedPatient") == "Welcome") {
      return true;
    }
    return false;
  },
  retIfPatient(){
    if(Session.get("SelectedPatient") != "") {
      return true;
    }
    return false;
  }
});
Template.body.events({
  'click .topnav'(input) {
    console.log("Input: " + input);
    console.log("Input target: " + input.target.getAttribute('id'));
    if(input.target.getAttribute('id') == "Dashboard") {
      Session.set("SelectedPatient", "Welcome");
    }
    else {
      Session.set("SelectedPatient", "");
    }
    if(input.target.getAttribute('id') != null)
      Session.set("FormVar", input.target.getAttribute('id'));
  }
  
});

Template.side.helpers({
  patients() {
    return Patients.find({});
  },
  returnSession(patient) {
    if(Session.get("SelectedPatient") == patient) {
      return true;
    }
    return false;
  }
});

Template.patientScreen.helpers({
  returnDates() {
    //console.log(Session.get("Dates"));
    return Session.get("Dates");
  },
  returnFiles(date){
    console.log("Date: " + date);
    patientName = Session.get("SelectedPatient").toLowerCase();
    doctor = Meteor.userId().toLowerCase();
    
    
    //Session.set("SelectedDate",date); //Set SelectedDate to current date clicked
    //console.log(Session.get("SelectedDate"));

    index = patientName.indexOf(" ");
    patientName = patientName.substring(0,index)+"-"+patientName.substring(index+1);
    bucketName = patientName+"_"+doctor+"_"+date;
    console.log(bucketName);
    Meteor.call('listFiles', bucketName ,
      (err, res) =>{
        if(err) {
          console.log("Error");
        }
        else{
          Session.set(date, res);
        }
      });
  },
  retFile(date) {
    console.log(Session.get("Files"));
    return Session.get(date);
  },
  returnURL(date, file){
    patientName = Session.get("SelectedPatient").toLowerCase();
    doctor = Meteor.userId().toLowerCase();
    index = patientName.indexOf(" ");
    patientName = patientName.substring(0,index)+"-"+patientName.substring(index+1);
    bucketName = patientName+"_"+doctor+"_"+String(date);
    // console.log("Bucket: " + bucketName);
    // console.log("Filename: " + file.name);
    Meteor.call('generateSignedUrl', bucketName , file.name , 
    (err, res) =>{
      if(err) {
        console.log("Error");
      }
      else{
        console.log(res);
        Session.set(String(date).concat(String(file.name)), String(res));
        //console.log("Result: " +)
      }
    });
  },
  retURL(date, file){
    console.log("Link: " +String(Session.get(String(date).concat(String(file.name)))));
    return String(Session.get(String(date).concat(String(file.name))));
  }
});

Template.side.events({
  "click .sidebar"(input) {
    //console.log("Input: " + input);
    //console.log("Input target: " + input.target.getAttribute('id'));
    if(input.target.getAttribute('id') != null)
      Session.set("SelectedPatient", input.target.getAttribute('id'));
    //console.log("Selected Patient" + Session.get("SelectedPatient"))
      //console.log(Meteor.call('getDates', String(Session.get("SelectedPatient"))));
    Meteor.call('testing', String(Session.get("SelectedPatient")) ,
      (err,res) =>{
        console.log("Result: " + res);
        Session.set("Dates", res);
      });
  },
  /*"select .dates"(input) {
    console.log("Selected: " + input.target);
  },*/
})


