import {get_query} from './common_funtions.js';

// POST call to 'vouchers/create' api to create vouchers with given name, price
export function createVoucher(vName, vPrice){
    fetch('/vouchers/create', get_query('POST', {
        vName: vName,
        vPrice: vPrice
    }))
    .then(response => {
        if (!response.ok) {
            throw new Error('POST request for create_voucher failed');
        }
        window.location.reload();
    })
    .catch(error => console.error(error));
}

// PUT call to 'voucher/<vNo>/details' API to edit voucher details for given vNo
export function editVoucherDetails(vNo, voucherName, voucherPrice){
    fetch(`/voucher/${vNo}/details`, get_query('PUT', {
        vNo: vNo,
        voucherName: voucherName,
        voucherPrice: voucherPrice
    }))
    .then(response => {
        if (!response.ok) {
            throw new Error('PUT request for editVoucherDetails failed');
        }
        window.location.reload();
    })
    .catch(error => console.error(error));
}

// PUT call to 'voucher/<vNo>/buy/<q>' API to buy voucher for given vNo
export function buyVoucher(vNo, q){
    fetch(`/voucher/${vNo}/buy/${q}`, get_query('PUT', {
        vNo: vNo,
        q: q
    }))
    .then(response => {
        if (!response.ok) {
            throw new Error('PUT request for edit_to_do failed');
        }
        window.location.reload();
    })
    .catch(error => console.error(error));
}

// PUT call to 'voucher/<vNo>/use/<q>' API to use voucher for given vNo
export function useVoucher(vNo, q){
    fetch(`/voucher/${vNo}/use/${q}`, get_query('PUT', {
        vNo: vNo,
        q: q
    }))
    .then(response => {
        if (!response.ok) {
            throw new Error('PUT request for edit_to_do failed');
        }
        window.location.reload();
    })
    .catch(error => console.error(error));
}

// // DELETE call to 'to_do/<taskNo>' API to delete TO DO with given no
// export function delete_to_do(taskNo){
//     fetch(`/to_do/${taskNo}`, get_query('DELETE'))
//     .then(response => {
//         if (!response.ok) {
//             throw new Error('DELETE request for delete_to_do failed');
//         }
//         window.location.reload();
//     })
//     .catch(error => console.error(error));
// }

// function for handling edit button in Vouchers
export function Voucher_edit_button_handler(_id) {
    if (document.getElementsByName('Voucher_name_' + _id)[0].contentEditable == 'true') {
        let voucherName = document.getElementsByName('Voucher_name_' + _id)[0].textContent;
        let voucherPrice = document.getElementsByName('Voucher_price_' + _id)[0].textContent;
        let vNo = _id;
        editVoucherDetails(vNo, voucherName, voucherPrice);
    }
    else {
        document.getElementsByName('Voucher_name_' + _id)[0].contentEditable = true;
        document.getElementsByName('Voucher_price_' + _id)[0].contentEditable = true;
    }
}

// Adds onclick function for 'createVouchers' popup's submit button
document.getElementById('createVoucher').addEventListener('click', function() {
    const vPrice = document.getElementById('Voucher_price').value;
    const vName = document.getElementById('Voucher_name').value;
    createVoucher(vName, vPrice);
});

// add click event listener to each button for editing Vouchers
const voucherEditBtns = document.querySelectorAll('#Voucher_edit_btn');
voucherEditBtns.forEach(button => {
    button.addEventListener('click', function() {
        const buttonNumber = parseInt(button.value);
        Voucher_edit_button_handler(buttonNumber);
    });
});

// add click event listener to each button for buying Vouchers
const voucherBuyBtns = document.querySelectorAll('#Voucher_buy_btn');
voucherBuyBtns.forEach(button => {
    button.addEventListener('click', function() {
        const buttonNumber = parseInt(button.value);
        buyVoucher(buttonNumber, 1);
    });
});

// add click event listener to each button for using Vouchers
const voucherUseBtns = document.querySelectorAll('#Voucher_use_btn');
voucherUseBtns.forEach(button => {
    button.addEventListener('click', function() {
        if (confirm('Really want to use Voucher?')){
            const buttonNumber = parseInt(button.value);
            useVoucher(buttonNumber, 1);
        }
    });
});

// // helper for filling parent cell in modal pop up in TO DO  
// const modal_new_TD = document.getElementById('modal_new_TD')
// modal_new_TD.addEventListener('show.bs.modal', event => {
//     // Button that triggered the modal
//     const button = event.relatedTarget
//     // Extract info from data-bs-* attributes
//     const parent = button.getAttribute('data-bs-parent')
//     // Update the modal's content.
//     const modalBodyInputParent = modal_new_TD.querySelector('#TD_parent')

//     modalBodyInputParent.value = parent
// })
