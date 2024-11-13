{
  pkgs,
  self,
  treefmtEval,
  ...
}:
{
  formatting = treefmtEval.config.build.check self;
}
