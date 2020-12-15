describe("Create Account Test", () => {
    it("Can fill the forms", () => {
        cy.visit("/createAccount");
        
        cy.get('input[type="radio"]')
            .check("student")
            .should("have.value", "student")
            .next().next().next().check()
            .should("have.value", "teacher");

        cy.get('input[name="username"]')
            .type("User012345")
            .should("have.value", "User012345");
        
        cy.get('input[name="email"]')
            .type("user012345@email.com")
            .should("have.value", "user012345@email.com");

        cy.get('input[name="password"]')
            .type("Password01")
            .should("have.value", "Password01");

        cy.get('input[name="password2"]')
            .type("Password01")
            .should("have.value", "Password01");


    });
});