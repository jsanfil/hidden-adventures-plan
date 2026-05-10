# Feature: iOS Notifications

## Summary

Add iOS push notifications as a retention and re-engagement feature with a narrow first-release scope.

## Status

- Program status: `Not Started`
- Completion source of truth: this document

## Scope

- broadcast release and update announcements
- nearby discovery notifications
- dormant-return notifications
- iOS push-permission flow
- minimum user-facing notification settings

## Dependencies

- stable authenticated app baseline
- device-token registration path
- backend notification delivery capability
- clear notification preference handling

## Delivery Gates

- [ ] Design accepted
- [ ] Mock iOS accepted
- [ ] Server accepted
- [ ] Integrated iOS accepted
- [ ] QA accepted

## Public Interface Expectations

- admin-triggered broadcast notification send path
- backend targeting and delivery logic for nearby discovery notifications
- backend targeting and delivery logic for dormant-return notifications
- iOS client notification handling and open-from-notification routing
- notification settings behavior that governs which notification categories a user receives

## QA And Proof

- [ ] UX notes linked where applicable
- [ ] SwiftUI gallery coverage updated where applicable
- [ ] notification permission handling verified
- [ ] each notification type verified with recorded proof
- [ ] open-from-notification routing validated
- [ ] notification settings enforcement validated
- [ ] integrated local happy path validated
- [ ] manual QA notes recorded

## Notes

- Keep v1 intentionally narrow around broadcast announcements, nearby discovery, and dormant-return notifications.
- Defer advanced segmentation, experiments, and broader lifecycle-marketing behavior unless they become explicit follow-on feature scope.
