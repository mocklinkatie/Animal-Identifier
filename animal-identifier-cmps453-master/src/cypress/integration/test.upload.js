// function to upload file using Cypress plugin 'cypress-file-upload'
const uploadFile = (fileName, fileType = '', selector) => {
    cy.get(selector).then(subject => {
      cy.fixture(fileName, 'base64')
        .then(Cypress.Blob.base64StringToBlob)
        .then(blob => {
          const el = subject[0]
          const testFile = new File([blob], fileName, { type: fileType })
          const dataTransfer = new DataTransfer()
          dataTransfer.items.add(testFile)
          el.files = dataTransfer.files
          console.log(el.files)
        })
    })
}

// filename to check
const fileName = 'butterfly2.jpg'

// actual test
describe("Test upload", () => {
    it("Can upload a photo", () => {
        cy.visit("/Upload");

        uploadFile(fileName, 'image/jpg', 'input[name="file"]');

        cy.get('input[type="submit"')
            .click();
        
        cy.url().should('eq', 'http://localhost:5000/Uploader')
        
    });
});
