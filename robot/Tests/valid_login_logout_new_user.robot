*** Settings ***
Documentation     A test suite with a tests for valid login, creating new user and logging out.
Resource          ../Common/resource.robot

*** Test Cases ***
Valid Login
    Open Browser To Login Page
    Input Username    admin admin
    Input Password    a
    Submit Credentials
    Welcome Page Should Be Open

New User
    Go To New User Creation
    Input New User Username    user2 user2
    Input New User Password    qqq
    Submit Credentials
    New User Page Should Be Open

Logout Try
    Logout
    Title Should Be    Grafiki - logowanie

Login With Created User
    Go To Login Page
    Input Username    user2 user2
    Input Password    qqq
    Submit Credentials
    Welcome Page Should Be Open
    Logout

Wrong Username
    Go To Login Page
    Input Username  wrong user
    Input Password  a
    Submit Credentials
    Check Wrong Login
    Title Should Be    Grafiki - logowanie

Wrong Password
    Go To Login Page
    Input Username  admin admin
    Input Password  b
    Submit Credentials
    Check Wrong Login
    Title Should Be    Grafiki - logowanie

Login Without User
    Go To Login Page
    Input Password  b
    Submit Credentials
    No User Or Password
    Title Should Be    Grafiki - logowanie

Login Without Password
    Go To Login Page
    Input Username  admin admin
    Submit Credentials
    No User Or Password
    Title Should Be    Grafiki - logowanie
    [Teardown]    Close Browser
