# Feature: Expanded Authentication

## Summary

Expand beyond the current email OTP baseline with additional sign-in options and device-auth capabilities.

## Status

- Program status: `Not Started`
- Completion source of truth: this document

## Scope

- phone-number sign-in
- Google sign-in
- Apple sign-in
- passkeys
- Face ID or biometric unlock where appropriate

## Dependencies

- stable baseline auth flow
- intentional identity and account-linking strategy
- platform and Cognito capability decisions

## Delivery Gates

- [ ] Design accepted
- [ ] Mock iOS accepted
- [ ] Server accepted
- [ ] Integrated iOS accepted
- [ ] QA accepted

## Public Interface Expectations

- auth surface additions for federation, phone, or passkey flows as chosen
- account-linking and session behavior updates
- QA coverage for returning-user and new-user identity branching

## QA And Proof

- [ ] UX notes linked
- [ ] SwiftUI gallery coverage updated where applicable
- [ ] server or auth-integration verification recorded
- [ ] integrated local happy path validated
- [ ] manual QA notes recorded

## Notes

- This is a dedicated later feature and should not silently mutate the current Slice 1 auth baseline while earlier product features are still landing.
