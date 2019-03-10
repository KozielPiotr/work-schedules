*** Settings ***
Documentation     A test suite with a tests for valid login, creating new user and logging out.
Resource          resource.robot

*** Test Cases ***
Valid Login
    Open Browser To Login Page
    Input Username    admin admin
    Input Password    a
    Submit Credentials
    Welcome Page Should Be Open

New User
    Go To New User Creation
    Input New User Username    user user
    Input New User Password    qqq
    Submit Credentials
    New User Page Should Be Open

Logout Try
    Logout
    Title Should Be    Grafiki - logowanie

Login With Created User
    Go To Login Page
    Input Username    user user
    Input Password    qqq
    Submit Credentials
    Welcome Page Should Be Open
    Logout
    [Teardown]    Close Browser
