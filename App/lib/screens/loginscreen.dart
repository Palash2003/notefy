// ignore_for_file: prefer_const_constructors, use_key_in_widget_constructors

import 'package:app/Providers/auth.dart';
import 'package:app/components/inputfield.dart';
import 'package:app/constants.dart';
import 'package:app/screens/mainscreen.dart';
import 'package:app/screens/registerscreen.dart';
import 'package:flutter/material.dart';
import 'package:app/components/roundedbutton.dart';

import 'dashboard.dart';

class LoginScreen extends StatefulWidget {
  static const String id = 'login_screen';
  @override
  _LoginScreenState createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  String email = '';
  String password = '';
  bool status = true;
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: kbgcolor,
      body: SingleChildScrollView(
        child: Container(
          padding: const EdgeInsets.only(
            top: 50,
            left: 20,
            right: 20,
            bottom: 10,
          ),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Padding(
                padding: const EdgeInsets.only(
                  top: 20,
                ),
                child: IconButton(
                  icon: Icon(
                    Icons.keyboard_arrow_left,
                    color: Colors.white,
                    size: 40,
                  ),
                  onPressed: () {
                    Navigator.pushNamed(context, MainScreen.id);
                  },
                ),
              ),
              Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  Flexible(
                    child: Image.asset(
                      'images/logo.png',
                      alignment: Alignment.center,
                      scale: 1.2,
                    ),
                  ),
                  SizedBox(
                    height: 50,
                  ),
                  InputField(
                      obscure: false,
                      hinttext: 'Email',
                      onChanged: (value) {
                        email = value;
                      }),
                  SizedBox(
                    height: 20,
                  ),
                  InputField(
                      obscure: true,
                      hinttext: 'Password',
                      onChanged: (value) {
                        password = value;
                      }),
                  SizedBox(
                    height: 20,
                  ),
                  RoundedButton(
                    onPressed: () async {
                      String token = await loginUser(email, password);
                      if (token == 'Error') {
                        setState(() {
                          status = false;
                        });
                      } else {
                        Navigator.pushNamed(
                          context,
                          DashBoard.id,
                        );
                      }
                    },
                    title: "Login",
                  ),
                  GestureDetector(
                    child: Text(
                      'New here? Register Now!',
                      textAlign: TextAlign.center,
                      style: TextStyle(
                        color: Colors.white,
                        fontSize: 16,
                      ),
                    ),
                    onTap: () {
                      Navigator.pushNamed(context, RegisterScreen.id);
                    },
                  ),
                  Text(status == false ? 'Unable To Login' : '',
                      style: TextStyle(color: Colors.white)),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }
}