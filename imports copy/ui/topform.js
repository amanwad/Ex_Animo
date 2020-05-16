import { Template } from 'meteor/templating';
import { ReactiveVar } from 'meteor/reactive-var';
import { Session } from 'meteor/session'
import { Mongo } from 'meteor/mongo'
import { Patients } from '../api/patients.js';
import './topform.html';

Template.form.helpers({

});

Template.form.events({
  'submit .new-patient': function(event) {
      // Prevent default browser form submit
      event.preventDefault();
      var name = event.target.name.value;
      var gender = event.target.gender.value;
      var blood = event.target.blood.value;
      var dob = event.target.birth.value;
      var pre = event.target.message.value;
      Meteor.call('addPatients',
       name,gender,dob,blood,pre, (err,res) => {
          console.log(res);
     });
      
  }
});
