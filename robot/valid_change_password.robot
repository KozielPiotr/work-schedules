*** Settings ***
Documentation     A test suite with a test for changing password.
Resource          resource.robot

*** Test Cases ***
Change Password
    Open Browser To Login Page
    Input Username    admin admin
    Input Password    a
    Submit Credentials
    Go To Password Change
    Input Current Password    a
    Input New Password    b
    Submit Credentials
    Logout
    Go To Login Page
    Input Username    admin admin
    Input Password    b
    Submit Credentials
    Welcome Page Should Be Open
    Go To Password Change
    Input Current Password    b
    Input New Password    a
    Submit Credentials
    [Teardown]    Close Browser
