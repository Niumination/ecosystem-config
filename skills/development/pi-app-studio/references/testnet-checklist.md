# Pi App — Testnet Pre-Submission Checklist

## Functional Testing

- [ ] App loads in Pi Browser (not regular browser)
- [ ] Pi Authentication works end-to-end
- [ ] User can sign in and see verified username
- [ ] All navigation works between pages
- [ ] Data displays correctly
- [ ] Search and filter work
- [ ] Payment flow completes (if applicable)
- [ ] Product delivery works after payment
- [ ] Incomplete payment recovery works

## Visual Testing

- [ ] App icon displays correctly (1024x1024)
- [ ] No layout issues on mobile (Pi Browser is mobile-first)
- [ ] Colors match design spec
- [ ] No overflow or truncation
- [ ] Loading states shown during API calls

## Security Testing

- [ ] No secrets in client-side code
- [ ] API key only in backend env var
- [ ] HTTPS enforced
- [ ] CORS configured correctly
- [ ] Input validation on all user inputs

## Performance Testing

- [ ] App loads in < 3 seconds
- [ ] API responses < 1 second
- [ ] No memory leaks on navigation
- [ ] Smooth scrolling on data tables

## Revenue Dashboard

- [ ] Revenue Dashboard shows in Pi Developer Portal
- [ ] Wallet address correctly configured
- [ ] Transaction history accessible
- [ ] Revenue share displayed correctly (Testnet: 100%)

## Before Mainnet Submission

- [ ] Minimum 2 weeks on Testnet with no critical bugs
- [ ] Production backend deployed (if using payments)
- [ ] Privacy policy and terms of service written
- [ ] App description and screenshots ready
- [ ] Support contact information provided
