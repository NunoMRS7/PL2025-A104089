program BubbleSortDemo;
var
  numbers: array[1..5] of integer;
  i, j, temp: integer;

procedure BubbleSort;
begin
  for i := 1 to 4 do
    for j := 1 to 5 - i do
      if numbers[j] > numbers[j + 1] then
      begin
        temp := numbers[j];
        numbers[j] := numbers[j + 1];
        numbers[j + 1] := temp;
      end;
end;

begin
  numbers[1] := 64;
  numbers[2] := 34;
  numbers[3] := 25;
  numbers[4] := 12;
  numbers[5] := 22;

  BubbleSort;

  for i := 1 to 5 do
    writeln(numbers[i]);
end.
