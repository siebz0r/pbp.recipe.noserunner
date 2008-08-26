#!/usr/bin/perl
use strict;
require 'limits.ph'; # UINT_MAX

# usage:
# ./make_size_lookup_h.pl
# created size_lookup_combo.h and size_lookup_permute.h
# which have lookup tables for the size of permute &
# combinations which are the largest we can handle
# (can't have an index > MAX_UINT, maximum value of an usnigned int)
#

my $high_n = UINT_MAX();

dump_stuff(gen_combo(\&combo_size, 80), 'combo_sizes', 'GET_COMBO_SIZE', 'size_lookup_combo.h');
dump_stuff(gen_permute(\&perm_size, 80), 'permute_sizes', 'GET_PERMUTE_SIZE', 'size_lookup_permute.h');

sub perm_size {
    my ($n, $k) = @_;

    my $tot = 1;
    for (my $i = $k; $i > 0; $i--) {
	$tot *= $i;
    }
    $tot *= combo_size($n,$k);
    return $tot;
}

sub combo_size { # calc n!/(k! * (n-k)!)
    my ($n, $k) = @_;

    my $tot = 1;
    my @mult = (($k+1) .. $n);
    my @div = (1 .. ($n - $k));
    my ($m, $d);
    while (@mult) {
        $m = shift(@mult);
        $d = shift(@div);
	$tot *= $m if $m;
	$tot /= $d if $d;
    }

    return $tot;
}

sub gen_combo {
    my $func = shift;
    my $max_col = shift;
    my $combo = [];
    my $padding = 0;

    my $n = 0;
    while ($n < $max_col) {
      my $row = [];
      for (my $k = 0; $k <= $n; $k++) {
	my $t = int(&$func($n, $k));
	if ($t < $high_n) {
	  push @$row, "${t}u"; # 1234u tells the compiler 1234 is unisgned
	} else {
	  push @$row, '0u';
	}
      }
      $padding = (@$row > $padding) ? @$row : $padding;
      push @$combo, $row;
      $n++;
    }
  DONE:

    # pad all the rows to padding length
    foreach my $nrow (@$combo) {
      while (@$nrow < $padding) {
        push @$nrow, 0;
      }
    }

    return $combo;
}


sub gen_permute {
    my $func = shift;
    my $max_col = shift;
    my $combo = [];
    my $padding = 0;

    my $n = 0;
    while ($n < $max_col) {
      my $row = [];
      for (my $k = 0; $k <= $n; $k++) {
	my $t = int(&$func($n, $k));
	if ($t < $high_n) {
	  push @$row, "${t}u"; # 1234u tells the compiler 1234 is unisgned
	}
      }
      $padding = (@$row > $padding) ? @$row : $padding;
      push @$combo, $row;
      $n++;
    }
  DONE:

    # pad all the rows to padding length
    foreach my $nrow (@$combo) {
      while (@$nrow < $padding) {
        push @$nrow, 0;
      }
    }

    return $combo;
}

sub dump_stuff {
    my $arrs = shift;
    my $struct_name = shift;
    my $def_name = shift;
    my $filename = shift;

    my ($i, $k) = (0+@$arrs, 0+@{$arrs->[0]});

    open(OF, ">$filename");
    print OF "#define $def_name(n,k) ((n < $i) ? ((k < $k) ? $struct_name\[n][k] : 0) : 0)\n";
    print OF "static unsigned int $struct_name\[$i][$k] = {\n";
    foreach my $row (@$arrs) {
      print OF '    { ', join(', ', @$row), " },\n";
    }
    print OF "};\n";
    close(OF);
}
