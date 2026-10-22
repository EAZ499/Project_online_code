const fs = require('fs');
const s = fs.readFileSync('1_ПЕРС_ХАРАКТ.rpy', 'utf8');
const lines = s.split('\n');
console.log(lines.slice(9255, 9265).join('\n'));