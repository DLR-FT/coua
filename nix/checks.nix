{
  pkgs,
  self,
  treefmtEval,
  ...
}:
{
  formatting = treefmtEval.${pkgs.system}.config.build.check self;
}
