use DateTime;
open IN, '<', 'so_edited.txt';
open OUT, '>', 'so_edited_with_RPMs.txt';

my $moreData = (my $line = <IN>);
chomp($line);
$dt = DateTime->from_epoch( epoch => $line );
$hour   = $dt->hour - 4; # 0-23
$minute = $dt->minute; # 0-59 - also 'min'
$second = $dt->second; # 0-61 (leap seconds!) - also 'sec'
my $rpm = 0;
print OUT "$hour:$minute:$second\t$rpm\n";

while($moreData)
{
  $moreData = (my $adj = <IN>);
  chomp($adj);
  $rpm = 60.0 / ($adj - $line);
  if (not defined($adj)) {next;}
  $dt = DateTime->from_epoch( epoch => $adj );
  $hour   = $dt->hour - 4; # 0-23
  $minute = $dt->minute; # 0-59 - also 'min'
  if ($minute < 10)
  {
    $minute = '0' . $minute;
  }
  $second = $dt->second; # 0-61 (leap seconds!) - also 'sec'
  if ($second < 10)
  {
    $second = '0' . $second;
  }

  print "$hour : $minute : $second\n";
  print OUT "$hour:$minute:$second\t$rpm\n";
  $line = $adj;
}
