 ########## Advanced TODO:, later, catch all cases well ####################
        # parens_ = re.split(r"\(\d+\)", palabra)
        # if len(parens_) > 1: # Weird case for the entry for 'a'
        #     p = Pala(parens_[0])
        #     for k, paren in enumerate(parens_[1:]):
        #         periodos_ = re.split(r"\d+\.", paren)
        #         origen = periodos_[0].replace('.','').strip()
        #         if not origen:
        #             origen = por_defecto
        #         p.defis[origen] = periodos_[1:]
        # else: # Typical case
        #     periodos_ = list(map(lambda x:x.strip(),re.split(r"\.", palabra)))
        #     p = Pala(periodos_[0])
        #     print(periodos_[0])
        #     print(periodos_[1:])
        #     p.defis[por_defecto] = periodos_[1:]
        ############################################################