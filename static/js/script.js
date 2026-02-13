document.addEventListener('DOMContentLoaded', () => {
    
    /* --- Mobile Menu Logic --- */
    const mobileMenuBtn = document.getElementById('mobileMenuBtn');
    const mobileMenu = document.getElementById('mobileMenu');
    const mobileIcon = mobileMenuBtn.querySelector('i');

    mobileMenuBtn.addEventListener('click', () => {
        const isShown = mobileMenu.classList.toggle('show');
        
        // Toggle Icon between Bars and X
        if(isShown) {
            mobileIcon.classList.remove('fa-bars');
            mobileIcon.classList.add('fa-xmark');
        } else {
            mobileIcon.classList.remove('fa-xmark');
            mobileIcon.classList.add('fa-bars');
        }
    });

    /* --- Profile Dropdown Logic --- */
    const profileBtn = document.getElementById('profileDropdownBtn');
    const profileDropdown = document.getElementById('profileDropdown');

    profileBtn.addEventListener('click', (e) => {
        e.stopPropagation(); // Prevent immediate closing
        profileDropdown.classList.toggle('show');
    });

    // Close dropdown when clicking outside
    document.addEventListener('click', (e) => {
        if (!profileBtn.contains(e.target) && !profileDropdown.contains(e.target)) {
            profileDropdown.classList.remove('show');
        }
    });

    /* --- Mock functionality for buttons --- */
    // const editBtn = document.querySelector('.edit-btn');
    // if (editBtn) {
    //     editBtn.addEventListener('click', () => {
    //         onclick="location.href='{% url 'update-profile' %}'";
    //     });
    // }

    // Highlight active nav link (Mock logic)
    const navLinks = document.querySelectorAll('.nav-link');
    // Assuming 'Members' is parent or we are just viewing Profile which isn't in main nav
    // Let's just highlight nothing or handle click
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            // e.preventDefault(); // In a real app we might prevent default
            navLinks.forEach(l => l.style.color = '#475569');
            this.style.color = 'var(--primary)';
        });
    });
});

/* --- Edit Profile Logic --- */
const avatarInput = document.getElementById('avatarInput');
const bannerInput = document.getElementById('bannerInput');

if (avatarInput) {
    avatarInput.addEventListener('input', (e) => {
        const url = e.target.value;
        const preview = document.getElementById('avatarPreview');
        if(url && preview) {
            preview.src = url;
            // Simple error handling for broken links
            preview.onerror = () => {
                // Keep old image or set a placeholder on error
                console.log("Invalid Image URL");
            };
        }
    });
}

if (bannerInput) {
    bannerInput.addEventListener('input', (e) => {
        const url = e.target.value;
        const preview = document.getElementById('bannerPreview');
        if(url && preview) {
            preview.src = url;
        }
    });
}

// const editForm = document.getElementById('editProfileForm');
// if(editForm) {
//     editForm.addEventListener('submit', (e) => {
//         e.preventDefault();
//         // In a real app, you would gather data here
//         alert("Changes Saved! Redirecting to Profile...");
//         window.location.href = "index.html";
//     });
// }

/* --- General Navigation Logic --- */
// (Add this to your existing script.js or ensure it doesn't conflict)

// Simple redirect for demo purposes
function navigateTo(page) {
    console.log("Navigating to:", page);
    // In a real static site, this would map to specific .html files
    // e.g., if(page === 'activities') window.location.href = 'activities.html';
}

// Add event listeners to any buttons with specific IDs if needed
// The HTML uses onclick="" attributes for simplicity in this demo,
// which is perfectly valid for a static prototype.

/* --- Auth Logic --- */

function togglePassword(inputId, btn) {
    const input = document.getElementById(inputId);
    const icon = btn.querySelector('i');
    
    if (input.type === "password") {
        input.type = "text";
        icon.classList.remove('fa-eye');
        icon.classList.add('fa-eye-slash');
    } else {
        input.type = "password";
        icon.classList.remove('fa-eye-slash');
        icon.classList.add('fa-eye');
    }
}

// Handle Login Submit
// const loginForm = document.getElementById('loginForm');
// if(loginForm) {
//     loginForm.addEventListener('submit', (e) => {
//         e.preventDefault();
//         const btn = loginForm.querySelector('.btn-loading');
        
//         // Show loading state
//         btn.classList.add('loading');
//         btn.disabled = true;

//         // Simulate API call
//         setTimeout(() => {
//             window.location.href = 'home.html';
//         }, 1000);
//     });
// }

// Handle Register Submit
// const registerForm = document.getElementById('registerForm');
// if(registerForm) {
//     registerForm.addEventListener('submit', (e) => {
//         e.preventDefault();
//         const btn = registerForm.querySelector('.btn-loading');
        
//         // Show loading state
//         btn.classList.add('loading');
//         btn.disabled = true;

//         // Simulate API call
//         setTimeout(() => {
//             // Redirect to Login after success (common pattern) 
//             // or directly to home. Using login for this flow.
//             window.location.href = 'login.html'; 
//         }, 1200);
//     });
// }


function toggleProfileDropdown() {
    const dropdown = document.getElementById('profileDropdown');
    dropdown.classList.toggle('show');
}

// Close dropdown when clicking outside
window.addEventListener('click', function(e) {
    const dropdown = document.getElementById('profileDropdown');
    const btn = document.querySelector('.profile-btn');
    const avatar = document.querySelector('.nav-avatar');

    // If the click is NOT on the button or the avatar, hide the dropdown
    if (e.target !== btn && e.target !== avatar) {
        if (dropdown && dropdown.classList.contains('show')) {
            dropdown.classList.remove('show');
        }
    }
});

