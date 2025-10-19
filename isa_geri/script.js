// Minimal JS: copy IBAN, open modal and placeholder for form link

document.addEventListener('DOMContentLoaded',()=>{
  const copyBtn = document.getElementById('copy-iban');
  const ibanEl = document.getElementById('iban');
  const openForm = document.getElementById('open-form');
  const modal = document.getElementById('modal');
  const modalClose = document.getElementById('modal-close');
  const modalFormLink = document.getElementById('modal-form-link');

  copyBtn.addEventListener('click', async ()=>{
    try{
      await navigator.clipboard.writeText(ibanEl.textContent.trim());
      copyBtn.textContent = 'Copiat!';
      setTimeout(()=>copyBtn.textContent='Copia',1500);
    }catch(e){
      alert('No s\'ha pogut copiar l\'IBAN. Copieu manualment.');
    }
  });

  openForm.addEventListener('click',(e)=>{
    e.preventDefault();
    // show modal with instruction and the same link
    modal.classList.remove('hidden');
    modal.setAttribute('aria-hidden','false');
    // set placeholder links - replace these later with your Google Form URL
    const placeholderLink = '#';
    openForm.setAttribute('href', placeholderLink);
    modalFormLink.setAttribute('href', placeholderLink);
  });

  modalClose.addEventListener('click',()=>{
    modal.classList.add('hidden');
    modal.setAttribute('aria-hidden','true');
  });
});
