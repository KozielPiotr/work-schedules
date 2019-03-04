*** Settings ***
Documentation     A test suite with a single test for valid login.
Resource          resource.robot

*** Test Cases ***
Valid Login
    Open Browser To Login Page
    Input Username    admin admin
    Input Password    a
    Submit Credentials
    Welcome Page Should Be Open
    [Teardown]    Close Browser
