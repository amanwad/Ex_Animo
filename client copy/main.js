import '../imports/ui/body.js';
//From Body.js


import '../imports/ui/topform.js';


//Aman's Code

import { Template } from 'meteor/templating';

import './main.html';

import { Accounts } from 'meteor/accounts-base';


import { Patients } from '../imports/api/patients.js';

import { Meteor } from 'meteor/meteor';

// Meteor.call('removeAllPatients',(err,res) =>{
//   console.log("removed all patients");
// });
console.log(Meteor.call('testing', String('Aman W')));
console.log(Patients);

// Meteor.call('testing', String('Aman W') ,
//  (err,res) =>{
//   console.log(res);
// });


Accounts.ui.config({
  passwordSignupFields:"USERNAME_ONLY"
  });
