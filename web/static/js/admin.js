
function navBarToggleOpen() {
    const sideBar = document.getElementById('sidebar');
    sideBar.style.display = 'flex';
    sideBar.style.transform = 'translateX(0%)';
    sideBar.style.zIndex = '2000'
    sideBar.style.transition = '0.3s'
};
function navBarToggleClose() {
    const sideBar = document.getElementById('sidebar');
    sideBar.style.display = 'flex';
    sideBar.style.transform = 'translateX(-100%)';
    sideBar.style.transition = '0.3s';;
};

function hideProductForm() {
    const productForm = document.getElementById('productModal');
    productForm.style.display = 'none';
    window.location.href = '/admin-product'
};

if (window.location.pathname === '/admin-product' || window.location.pathname ==='/admin-orders') {
    
    const search = document.getElementById('searchProduct'),
        table_rows = document.querySelectorAll('tbody tr');
    
    search.addEventListener('input', searchTable);
    
    function searchTable() {
        table_rows.forEach((row, i) => {
            let table_data = row.textContent.toLowerCase(),
            search_data = search.value.toLowerCase();
    
            row.classList.toggle('hide', table_data.indexOf(search_data) < 0);
            row.style.setProperty('--delay', i/25 + 's');
        });
    };
}

const activePage = window.location.pathname;
const navLinks = document.querySelectorAll('nav a').forEach(link => {
    if (link.href.includes(`${activePage}`)) {
        link.classList.add('active')
    }
})

if (window.location.pathname.includes('update-product')) {
    const closeModal = document.getElementById('closeModal');
    closeModal.addEventListener('click', event => {
        const updatForm = document.querySelector('.modal.show');
        updatForm.style.display = 'none';
        window.location.href = '/admin-product';
    });
    const cancelModal = document.getElementById('cancelModal');
    cancelModal.addEventListener('click', event => {
        const updatForm = document.querySelector('.modal.show');
        updatForm.style.display = 'none';
        window.location.href = '/admin-product';
    });
}

if (window.location.pathname.includes('update-order-status')) {
    const closeOrderModal = document.getElementById('closeOrderModal');
    closeOrderModal.addEventListener('click', event => {
        const updatOrderForm = document.querySelector('.modal.show');
        updatOrderForm.style.display = 'none';
        window.location.href = '/admin-orders';
    });
    const cancelOrderModal = document.getElementById('cancelOrderModal');
    cancelOrderModal.addEventListener('click', event => {
        const updatForm = document.querySelector('.modal.show');
        updatForm.style.display = 'none';
        window.location.href = '/admin-orders';
    });
}

if (window.location.pathname.includes('add-brand')) {
    const closeBrandModal = document.getElementById('closeBrandModal');
    closeBrandModal.addEventListener('click', event => {
        const brandForm = document.querySelector('.modal.show');
        brandForm.style.display = 'none';
        window.location.href = '/admin-brands';
    });
    const cancelbrandModal = document.getElementById('cancelBrandModal');
    cancelbrandModal.addEventListener('click', event => {
        const add_brandForm = document.querySelector('.modal.show');
        add_brandForm.style.display = 'none';
        window.location.href = '/admin-brands';
    });
}