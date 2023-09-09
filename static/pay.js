var stripe = Stripe(checkout_public_key);

const BasicButton = document.querySelector('#basicButton');
const IntermediateButton = document.querySelector('#intermediateButton');
const EliteButton = document.querySelector('#eliteButton');
const UltimateButton = document.querySelector('#ultimateButton');

BasicButton.addEventListener('click', event => {
    stripe.redirectToCheckout({
        sessionId: checkout_session_basic_id // Use the correct session ID for Basic
    }).then(function (result){

    })
})

IntermediateButton.addEventListener('click', event => {
    stripe.redirectToCheckout({
        sessionId: checkout_session_intermediate_id // Use the correct session ID for Intermediate
    }).then(function (result){

    })
})

EliteButton.addEventListener('click', event => {
    stripe.redirectToCheckout({
        sessionId: checkout_session_elite_id // Use the correct session ID for Elite
    }).then(function (result){

    })
})

UltimateButton.addEventListener('click', event => {
    stripe.redirectToCheckout({
        sessionId: checkout_session_ultimate_id // Use the correct session ID for Ultimate
    }).then(function (result){

    })
})
