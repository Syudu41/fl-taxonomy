/* Small learning and library interactions; all reading content remains Markdown. */
const rate = document.querySelector('#learning-rate');
if (rate) {
  const update = () => {
    const eta = Number(rate.value);
    const weight = 1 + 8 * eta;
    const loss = (2 * weight - 4) ** 2;
    document.querySelector('#rate-value').value = eta.toFixed(3);
    document.querySelector('#new-weight').textContent = weight.toFixed(3);
    document.querySelector('#new-loss').textContent = loss.toFixed(3);
    document.querySelector('#step-explanation').textContent = eta === 0
      ? 'With a zero learning rate, the parameter and loss do not change.'
      : loss < 0.000001 ? 'For this example, the step lands exactly at w = 2 and the training loss is zero.'
      : loss < 4 ? 'This step lowers the training loss on the one example. It does not establish generalization.'
      : loss > 4 ? 'The step overshoots far enough to increase the loss. A larger learning rate is not always better.'
      : 'The parameter changes, but this step leaves the loss at its starting value.';
  };
  rate.addEventListener('input', update);
  update();
}
const search = document.querySelector('#paper-search');
if (search) {
  const kind = document.querySelector('#paper-kind');
  const records = [...document.querySelectorAll('.paper-record')];
  const filter = () => {
    const terms = search.value.toLocaleLowerCase().trim().split(/\s+/).filter(Boolean);
    let shown = 0;
    for (const record of records) {
      const haystack = record.dataset.search.toLocaleLowerCase();
      record.hidden = !(terms.every(term => haystack.includes(term)) && (!kind.value || record.dataset.kind === kind.value));
      if (!record.hidden) shown++;
    }
    document.querySelector('#paper-filter-result').textContent = shown ? `${shown} of ${records.length} records` : 'No papers match. Try a different title, author, or topic.';
  };
  search.addEventListener('input', filter);
  kind.addEventListener('change', filter);
  filter();
  document.querySelectorAll('.copy-citation').forEach(button => button.addEventListener('click', async () => {
    const record = button.closest('.paper-record');
    const citation = record.querySelector('.bibtex-source').textContent.trim();
    try {
      await navigator.clipboard.writeText(citation);
      button.textContent = 'Copied';
      setTimeout(() => { button.textContent = 'Copy BibTeX'; }, 1600);
    } catch {
      record.querySelector('.citation-details').open = true;
      const selection = window.getSelection();
      const range = document.createRange();
      range.selectNodeContents(record.querySelector('.bibtex-source'));
      selection.removeAllRanges();selection.addRange(range);
      button.textContent = 'Select and copy citation below';
    }
  }));
}
