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
    return "Doctor ID: " + Meteor.userId();
  }
});
Template.body.events({
  'click .topnav'(input) {
    console.log("Input: " + input);
    console.log("Input target: " + input.target.getAttribute('id'));
    if(input.target.getAttribute('id') != null)
      Session.set("FormVar", input.target.getAttribute('id'));
  },
  'click .dropbtn'(input) {
    console.log("Selected Patient" + Session.get("SelectedPatient"))
    //console.log(Meteor.call('getDates', String(Session.get("SelectedPatient"))));
    Meteor.call('testing', String('Aman W') ,
     (err,res) =>{
      //console.log(res);
      Session.set("Dates", res);
    });
  },
  
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
  },
  returnDates() {
    console.log(Session.get("Dates"));
    return Session.get("Dates");
  },
  returnFiles(){
    console.log("Good morning!");
    console.log(Session.get("Files"));
    return Session.get("Files");
  },
  myDate(date){
    //console.log("Good Morning: "+ date);
    console.log(date + ": " + String(Session.get("SelectedDate") == date));
    if(Session.get("SelectedDate") == date){
      return true;
    }
    return false;
  },
  retDrop() {
    return Session.get("Dropped");
  }
});

Template.side.events({
  "click .sidebar"(input) {
    console.log("Input: " + input);
    console.log("Input target: " + input.target.getAttribute('id'));
    if(input.target.getAttribute('id') != null)
      Session.set("SelectedPatient", input.target.getAttribute('id'));
  },
  /*"select .dates"(input) {
    console.log("Selected: " + input.target);
  },*/
  'click .dropbtn'(event) {
    Session.set("Dropped", true);
  },
  'click .datebtn'(event) {
    event.preventDefault();
    patientName = Session.get("SelectedPatient").toLowerCase();
    doctor = Meteor.userId().toLowerCase();
    date = event.target.getAttribute('id');
    
    
    Session.set("SelectedDate",date); //Set SelectedDate to current date clicked
    //console.log(Session.get("SelectedDate"));

    index = patientName.indexOf(" ");
    patientName = patientName.substring(0,index)+"-"+patientName.substring(index+1);
    bucketName = patientName+"_"+doctor+"_"+date;
    Meteor.call('listFiles', bucketName ,
      (err, res) =>{
        Session.set("Files", res);
      });
  }
})

//Non-Meteor Javascr