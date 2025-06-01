program RecursiveFactorial;
var
  n: integer;

function Factorial(x: integer): integer;
begin
  if x = 0 then
    Factorial := 1
  else
    Factorial := x * Factorial(x - 1);
end;

begin
  writeln('Enter a non-negative integer:');
  readln(n);

  if n < 0 then
    writeln('Error: Negative numbers are not allowed!')
  else
    writeln('Factorial of ', n, ' is ', Factorial(n));
end.
