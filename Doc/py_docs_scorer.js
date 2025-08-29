
var Scorer = {
    // Implement the following function to further tweak the score for each result
    score: result => {
      let [docname, title, anchor, descr, score, filename] = result
        console.log(result);
      if (docname == 'library/stdtypes'){
          // try to elevate built-in types
          score += 10;
      }

      return score
    },

    // query matches the full name of an object
    objNameMatch: 20,
    // or matches in the last dotted part of the object name
    objPartialMatch: 6,
    // Additive scores depending on the priority of the object
    objPrio: {
      0: 15, // used to be importantResults
      1: 5, // used to be objectResults
      2: -5, // used to be unimportantResults
    },
    //  Used when the priority is not in the mapping.
    objPrioDefault: 0,

    // query found in title
    title: 15,
    partialTitle: 7,

    // query found in terms
    term: 5,
    partialTerm: 2,
};
